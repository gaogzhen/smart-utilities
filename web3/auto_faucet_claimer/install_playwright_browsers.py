#!/usr/bin/env python3
"""将 Playwright Chromium 安装到项目目录 .playwright-browsers，与 faucet_claimer 使用的路径一致。"""
import os
import subprocess
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
browsers_path = os.path.join(script_dir, ".playwright-browsers")
os.environ["PLAYWRIGHT_BROWSERS_PATH"] = browsers_path

print(f"Playwright 浏览器将安装到: {browsers_path}")
print("正在安装 Chromium …")
r = subprocess.run(
    [sys.executable, "-m", "playwright", "install", "chromium"],
    env={**os.environ},
)
sys.exit(r.returncode)
