# scheduler.py
import asyncio
import schedule
import time
from datetime import datetime
from faucet_claimer import main as run_claimer


def job():
    """包装异步任务给schedule调用"""
    print(f"\n⏰ 触发定时任务 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    asyncio.run(run_claimer())


def run_scheduler():
    """设置并运行定时调度"""
    # 示例：每天上午10:15运行
    schedule.every().day.at("10:15").do(job)

    # 或者每24小时运行一次
    # schedule.every(24).hours.do(job)

    print("✅ 自动水龙头领取调度器已启动")
    print(f"下次运行时间: {schedule.next_run()}")
    print("程序将在后台运行，按 Ctrl+C 退出\n")

    while True:
        schedule.run_pending()
        time.sleep(60)  # 每分钟检查一次


if __name__ == "__main__":
    # 也可以直接运行一次进行测试
    # asyncio.run(run_claimer())

    # 启动定时调度
    run_scheduler()