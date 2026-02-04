# faucet_claimer.py
import os
import sys

# 在导入 crawl4ai/playwright 之前指定浏览器路径，使用项目内目录，避免与系统缓存路径不一致导致找不到浏览器
_script_dir = os.path.dirname(os.path.abspath(__file__))
os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH", os.path.join(_script_dir, ".playwright-browsers"))

import asyncio
import json
import time
from datetime import datetime, timedelta
from crawl4ai import AsyncWebCrawler
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig
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

    async def execute_steps(self, page, steps, faucet_name):
        """执行预定义的步骤序列。page 为 Playwright Page 对象（由 _get_page(crawler) 获取）。"""
        if not page:
            print("  ❌ 无法获取当前页面，跳过步骤")
            return
        for step in steps:
            print(f"  -> 步骤: {step.get('description', 'N/A')}")
            action = step.get("action")

            if action == "type":
                selector = step["selector"]
                value = step["value"]
                await page.type(selector, value)
                await asyncio.sleep(1)

            elif action == "click":
                selector = step["selector"]
                await page.click(selector)
                await asyncio.sleep(2)

            elif action == "select":
                selector = step["selector"]
                value = step["value"]
                await page.select_option(selector, value)
                await asyncio.sleep(1)

            elif action == "wait_for_text":
                text = step["text"]
                timeout_ms = step.get("timeout", 10) * 1000
                try:
                    await page.get_by_text(text).first.wait_for(state="visible", timeout=timeout_ms)
                except Exception:
                    print(f"    警告: 未在 {timeout_ms // 1000}s 内找到文本 '{text}'")

            elif action == "solve_captcha":
                # 遇到验证码时，暂停脚本，等待用户手动操作
                print(f"\n⚠️  请在浏览器中手动解决验证码 ({faucet_name})...")
                print("    解决后，请在控制台按回车键继续...")
                input()  # 阻塞，等待用户手动操作后按回车
                await asyncio.sleep(3)

            await asyncio.sleep(1)  # 步骤间基础间隔

    def check_success(self, result_or_html, success_indicators):
        """根据配置的成功指标，判断领取是否成功。result_or_html 可为带 .html 的对象或 HTML 字符串。"""
        html = result_or_html.html if hasattr(result_or_html, "html") else result_or_html
        html_lower = (html or "").lower()
        for indicator in success_indicators:
            ind_type = indicator["type"]

            if ind_type == "text_in_page":
                if indicator["content"].lower() in html_lower:
                    return True

            elif ind_type == "element_present":
                if indicator["selector"] in (html or ""):
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

        # 2. 使用 Crawl4AI 启动浏览器，直接拿 page 并自行 goto，避免 arun 结束后页面被关闭
        async with AsyncWebCrawler(config=self.browser_config) as crawler:
            try:
                run_config = CrawlerRunConfig(url=faucet["url"])
                page, _ = await crawler.crawler_strategy.browser_manager.get_page(run_config)
                await page.goto(faucet["url"], wait_until="domcontentloaded", timeout=30000)
                await asyncio.sleep(3)  # 等待页面稳定（如 wait_for 效果）

                # 领取步骤可能较慢（网络/弹窗/验证码），将页面操作默认超时设为 2 分钟
                page.set_default_timeout(120000)

                # 3. 在当前页执行预定义的领取步骤（page 不会被 arun 关闭）
                await self.execute_steps(page, faucet.get("steps", []), faucet_name)

                # 4. 从当前页取 HTML 判断是否成功，不再调用 arun 避免新建/关闭页面
                html = await page.content()
                if self.check_success(html, faucet.get("success_indicators", [])):
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

    async def run(self):
        """遍历并处理所有水龙头"""
        print(f"=== 开始领取任务 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===")
        for faucet in FAUCET_TASKS:
            await self.claim_single_faucet(faucet)
            await asyncio.sleep(5)  # 水龙头间间隔，避免请求过快
        print("=== 领取任务结束 ===\n")


async def run_manual_demo(faucet=None):
    """
    手动演示模式：打开浏览器并加载水龙头页面，暂停等待你手动操作一遍。
    操作完成后在控制台按回车结束。请记下你点击的按钮文字、输入框位置等，便于后续编写自动化步骤。
    """
    faucet = faucet or (FAUCET_TASKS[0] if FAUCET_TASKS else None)
    if not faucet:
        print("❌ 没有可用的水龙头任务")
        return

    print(f"\n📌 手动演示模式: {faucet['name']}")
    print(f"   URL: {faucet['url']}")
    print("\n" + "=" * 60)
    print("  请在浏览器中手动完成一次领取，例如：")
    print("  1. 连接钱包（如 MetaMask）")
    print("  2. 选择网络 / 选择代币")
    print("  3. 如需要可输入或确认钱包地址")
    print("  4. 完成人机验证（如有）")
    print("  5. 点击 Claim 领取")
    print("=" * 60)
    print("  完成后请回到本窗口，按 回车 结束演示。\n")

    async with AsyncWebCrawler(config=BrowserConfig(headless=False, proxy=PROXY if PROXY else None)) as crawler:
        run_config = CrawlerRunConfig(url=faucet["url"])
        page, _ = await crawler.crawler_strategy.browser_manager.get_page(run_config)
        # 手动演示不设超时，避免页面加载或操作过程中被超时中断
        await page.goto(faucet["url"], wait_until="domcontentloaded", timeout=0)
        await asyncio.sleep(2)

        # 阻塞，等用户手动操作后按回车
        input(">>> 按回车键结束演示并关闭浏览器 ... ")

    print("演示结束。可根据你刚才的操作，把步骤（按钮文字、选择器）告诉我，我会更新 config 中的 steps。\n")


async def main():
    # 支持 --manual / --demo：只打开浏览器，等你手动操作一遍后按回车
    if "--manual" in sys.argv or "--demo" in sys.argv:
        await run_manual_demo()
        return

    claimer = FaucetClaimer()
    await claimer.run()


if __name__ == "__main__":
    asyncio.run(main())