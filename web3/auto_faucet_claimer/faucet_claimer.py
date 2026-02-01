# faucet_claimer.py
import asyncio
import json
import time
from datetime import datetime, timedelta
from crawl4ai import AsyncWebCrawler
from crawl4ai.async_configs import BrowserConfig
from config import FAUCET_TASKS, WALLET_ADDRESS, PROXY


class FaucetClaimer:
    def __init__(self):
        # 加载领取历史记录
        self.history_file = "claim_history.json"
        self.history = self.load_history()
        self.browser_config = BrowserConfig(
            headless=False,  # 首次调试设为False可以看到浏览器操作，稳定后改为True
            proxy=PROXY if PROXY else None
        )

    def load_history(self):
        """加载历史领取记录"""
        try:
            with open(self.history_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}  # 首次运行，历史记录为空

    def save_history(self):
        """保存历史领取记录"""
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=4)

    def can_claim(self, faucet_name):
        """检查是否满足24小时间隔"""
        if faucet_name not in self.history:
            return True
        last_claimed_str = self.history[faucet_name].get("last_claimed")
        if not last_claimed_str:
            return True

        last_claimed = datetime.fromisoformat(last_claimed_str)
        time_since_last = datetime.now() - last_claimed
        return time_since_last > timedelta(hours=24)

    async def execute_steps(self, crawler, steps, faucet_name):
        """执行预定义的步骤序列"""
        for step in steps:
            print(f"  -> 步骤: {step.get('description', 'N/A')}")
            action = step.get("action")

            if action == "type":
                selector = step["selector"]
                value = step["value"]
                await crawler.page.type(selector, value)
                await asyncio.sleep(1)

            elif action == "click":
                selector = step["selector"]
                await crawler.page.click(selector)
                await asyncio.sleep(2)

            elif action == "select":
                selector = step["selector"]
                value = step["value"]
                await crawler.page.select_option(selector, value)
                await asyncio.sleep(1)

            elif action == "wait_for_text":
                text = step["text"]
                timeout = step.get("timeout", 10) * 1000  # 转毫秒
                try:
                    await crawler.page.wait_for_selector(f"text={text}", timeout=timeout)
                except:
                    print(f"    警告: 未在页面中找到文本 '{text}'")

            elif action == "solve_captcha":
                # 遇到验证码时，暂停脚本，等待用户手动操作
                print(f"\n⚠️  请在浏览器中手动解决验证码 ({faucet_name})...")
                print("    解决后，请在控制台按回车键继续...")
                input()  # 阻塞，等待用户手动操作后按回车
                await asyncio.sleep(3)

            await asyncio.sleep(1)  # 步骤间基础间隔

    def check_success(self, result, success_indicators):
        """根据配置的成功指标，判断领取是否成功"""
        html_lower = result.html.lower()
        for indicator in success_indicators:
            ind_type = indicator["type"]

            if ind_type == "text_in_page":
                if indicator["content"].lower() in html_lower:
                    return True

            elif ind_type == "element_present":
                # 这里可以扩展为使用crawler检查元素是否存在
                if indicator["selector"] in result.html:
                    return True
        return False

    async def claim_single_faucet(self, faucet):
        """领取单个水龙头"""
        faucet_name = faucet["name"]

        # 1. 检查时间间隔
        if not self.can_claim(faucet_name):
            wait_until = datetime.fromisoformat(self.history[faucet_name]["last_claimed"]) + timedelta(hours=24)
            print(f"⏸️  跳过 {faucet_name}，下次可领取时间: {wait_until.strftime('%Y-%m-%d %H:%M')}")
            return False

        print(f"\n🚀 开始处理: {faucet_name}")

        # 2. 使用Crawl4AI启动浏览器会话
        async with AsyncWebCrawler(config=self.browser_config) as crawler:
            try:
                # 访问页面
                result = await crawler.arun(url=faucet["url"], wait_for=3000)
                if not result.success:
                    print(f"❌ 页面加载失败: {faucet_name}")
                    return False

                # 3. 执行预定义的领取步骤
                await self.execute_steps(crawler, faucet.get("steps", []), faucet_name)

                # 4. 获取最终页面结果，判断是否成功
                final_result = await crawler.arun(url=crawler.page.url, bypass_cache=True)

                if self.check_success(final_result, faucet.get("success_indicators", [])):
                    # 领取成功，更新历史记录
                    self.history[faucet_name] = {
                        "last_claimed": datetime.now().isoformat(),
                        "network": faucet["network"]
                    }
                    self.save_history()
                    print(f"✅ 成功领取 {faucet_name}!")
                    return True
                else:
                    print(f"⚠️  领取可能未成功: {faucet_name} (未检测到成功标志)")
                    return False

            except Exception as e:
                print(f"❌ 处理 {faucet_name} 时出错: {e}")
                return False
            finally:
                # 确保页面关闭
                await crawler.close()

    async def run(self):
        """遍历并处理所有水龙头"""
        print(f"=== 开始领取任务 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===")
        for faucet in FAUCET_TASKS:
            await self.claim_single_faucet(faucet)
            await asyncio.sleep(5)  # 水龙头间间隔，避免请求过快
        print("=== 领取任务结束 ===\n")


async def main():
    claimer = FaucetClaimer()
    await claimer.run()


if __name__ == "__main__":
    asyncio.run(main())