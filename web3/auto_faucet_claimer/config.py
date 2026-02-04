# config.py
import os

# 你的测试钱包地址
WALLET_ADDRESS = "0x1b085cB185CE7340731D641AEA498F49c5F6d85b"

# 可选：代理设置，防止IP被封，可从环境变量读取
PROXY = os.getenv("PROXY_URL")  # 格式如: http://user:pass@host:port

# 水龙头任务列表 (手动收集和配置的核心部分)
# 常用测试网水龙头参考:
#   - Ethereum Sepolia: https://sepolia-faucet.pk910.de/ 或 https://www.alchemy.com/faucets/ethereum-sepolia
#   - Avalanche Fuji:   https://core.app/tools/testnet-faucet/?subnet=avax&chain=fuji
#   - Polygon Amoy:     https://faucet.polygon.technology/
#   - Chainlink:        https://faucets.chain.link/
# 添加新任务时需在浏览器中确认选择器与成功文案，步骤支持: type / click / select / wait_for_text / solve_captcha
# 若页面需先连接 MetaMask，可配置 wallet_connect：领取前会检测是否已连接，未连接则自动点击连接并处理 MetaMask 弹窗
FAUCET_TASKS = [
{
        "name": "Core.app Avalanche Fuji Faucet",
        "url": "https://core.app/tools/testnet-faucet/?subnet=avax&chain=fuji",
        "network": "Avalanche Fuji (C-Chain)",
        # 领取前检测并自动连接 MetaMask（可选）
        "wallet_connect": {
            "connect_button_selector": "button:has-text('Connect Wallet')",
            "connected_indicator": {"type": "text_in_page", "content": "Connected"},
            "metamask_popup": {
                "next_button": "button:has-text('Next')",
                "connect_button": "button:has-text('Connect')",
                "timeout": 15000,
            },
        },
        "steps": [
            {
                "action": "click",
                "selector": "button:has-text('Next')",
                "description": "选择网络"
            },
            {
                "action": "click",
                "selector": "button:has-text('Next')",
                "description": "选择token"
            },
            {
                "action": "type",
                "selector": "input[placeholder*='Address'], input[type='text']",
                "value": WALLET_ADDRESS,
                "description": "输入钱包地址（若页面已显示地址可跳过）"
            },
            {
                "action": "solve_captcha",
                "description": "reCAPTCHA 人机验证：在浏览器中完成验证后按回车继续"
            },
            {
                "action": "click",
                "selector": "button:has-text('Claim')",  # 领取按钮
                "description": "点击Claim按钮领取AVAX"
            },
            {
                "action": "wait_for_text",
                "text": "Claimed",  # 或其他成功提示词
                "timeout": 30,
                "description": "等待领取成功提示"
            }
        ],
        "success_indicators": [
            {
                "type": "text_in_page",
                "content": "Claimed"  # 页面出现此文本即认为成功
            },
            {
                "type": "text_in_page",
                "content": "Transaction sent"  # 或交易已发送
            },
            {
                "type": "element_present",
                "selector": "a[href*='snowtrace.io']"  # 出现Snowtrace（AVAX浏览器）链接
            }
        ]
    }
    # {
    #     "name": "Sepolia 水龙头",
    #     "url": "https://sepolia-faucet.pk910.de/",
    #     "network": "Ethereum Sepolia",
    #     # 自定义的领取步骤 (CSS选择器)
    #     "steps": [
    #         {"action": "type", "selector": "input[type='text']", "value": WALLET_ADDRESS,
    #          "description": "输入钱包地址"},
    #         {"action": "click", "selector": "button[type='submit']", "description": "点击提交按钮"},
    #         {"action": "wait_for_text", "text": "funded", "timeout": 30, "description": "等待到账成功提示"}
    #     ],
    #     # 成功领取后的判断依据 (满足其一即可)
    #     "success_indicators": [
    #         {"type": "text_in_page", "content": "successfully funded"},
    #         {"type": "text_in_page", "content": "Transaction sent"}
    #     ]
    # },
    # {
    #     "name": "avax 水龙头",
    #     "url": "https://core.app/tools/testnet-faucet",
    #     "network": "avalanche ",
    #     "steps": [
    #         {"action": "select", "selector": "select[name='network']", "value": "mumbai",
    #          "description": "选择Mumbai网络"},
    #         {"action": "type", "selector": "input[name='address']", "value": WALLET_ADDRESS,
    #          "description": "输入钱包地址"},
    #         {"action": "click", "selector": "button:has-text('Submit')", "description": "点击提交"},
    #         {"action": "solve_captcha", "description": "等待手动解决验证码"},  # 特殊步骤，会暂停脚本
    #     ],
    #     "success_indicators": [
    #         {"type": "element_present", "selector": ".alert-success"}
    #     ]
    # },
    # {
    #     "name": "chainlist 平台水龙头",
    #     "url": "https://faucets.chain.link/",
    #     "network": "",
    #     "steps": [
    #         {"action": "select", "selector": "select[name='network']", "value": "mumbai",
    #          "description": "选择Mumbai网络"},
    #         {"action": "type", "selector": "input[name='address']", "value": WALLET_ADDRESS,
    #          "description": "输入钱包地址"},
    #         {"action": "click", "selector": "button:has-text('Submit')", "description": "点击提交"},
    #         {"action": "solve_captcha", "description": "等待手动解决验证码"},  # 特殊步骤，会暂停脚本
    #     ],
    #     "success_indicators": [
    #         {"type": "element_present", "selector": ".alert-success"}
    #     ]
    # },
    # {
    #     "name": "polygon 水龙头",
    #     "url": "https://faucet.polygon.technology/",
    #     "network": "",
    #     "steps": [
    #         {"action": "select", "selector": "select[name='network']", "value": "mumbai",
    #          "description": "选择Mumbai网络"},
    #         {"action": "type", "selector": "input[name='address']", "value": WALLET_ADDRESS,
    #          "description": "输入钱包地址"},
    #         {"action": "click", "selector": "button:has-text('Submit')", "description": "点击提交"},
    #         {"action": "solve_captcha", "description": "等待手动解决验证码"},  # 特殊步骤，会暂停脚本
    #     ],
    #     "success_indicators": [
    #         {"type": "element_present", "selector": ".alert-success"}
    #     ]
    # }, {
    #     "name": "polygon 水龙头",
    #     "url": "https://faucet.polygon.technology/",
    #     "network": "",
    #     "steps": [
    #         {"action": "select", "selector": "select[name='network']", "value": "mumbai",
    #          "description": "选择Mumbai网络"},
    #         {"action": "type", "selector": "input[name='address']", "value": WALLET_ADDRESS,
    #          "description": "输入钱包地址"},
    #         {"action": "click", "selector": "button:has-text('Submit')", "description": "点击提交"},
    #         {"action": "solve_captcha", "description": "等待手动解决验证码"},  # 特殊步骤，会暂停脚本
    #     ],
    #     "success_indicators": [
    #         {"type": "element_present", "selector": ".alert-success"}
    #     ]
    # },

    # 你可以继续按此格式添加更多水龙头...
    # {
    #   "name": "...",
    #   "url": "...",
    #   "steps": [...],
    #   "success_indicators": [...]
    # }
]
