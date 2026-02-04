# 从 Faucet 获取区块链测试币方案

本方案通过**浏览器自动化**访问各类测试网水龙头页面，按配置的步骤自动完成「输入地址 → 选择网络/代币 → 点击领取」等操作，并支持定时执行与 24 小时冷却，实现从 Faucet 稳定获取测试币。

---

## 一、方案概述

| 项目 | 说明 |
|------|------|
| **目标** | 从多个区块链测试网水龙头自动领取测试币到指定钱包 |
| **方式** | 使用 [Crawl4AI](https://github.com/unclecode/crawl4ai) 驱动真实浏览器，模拟用户操作 |
| **适用** | 支持「输入地址 + 点击」的网页水龙头；需验证码的可配置为手动介入 |
| **冷却** | 每个水龙头单独记录领取时间，默认 24 小时内不重复领取 |

---

## 二、架构与流程

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  config.py      │────▶│  faucet_claimer  │────▶│  各水龙头网页   │
│  钱包/任务配置   │     │  执行步骤+判断   │     │  (浏览器访问)   │
└─────────────────┘     └────────┬─────────┘     └─────────────────┘
                                 │
                                 ▼
                        ┌──────────────────┐
                        │ claim_history    │
                        │ 24h 冷却记录     │
                        └──────────────────┘
                                 ▲
┌─────────────────┐     ┌───────┴──────────┐
│  scheduler.py   │────▶│  定时触发任务     │
│  每日/周期执行   │     │  (如每天 10:15)   │
└─────────────────┘     └──────────────────┘
```

1. **配置**：在 `config.py` 中填写钱包地址、可选代理，以及每个水龙头的 URL 和操作步骤。
2. **执行**：`faucet_claimer.py` 依次处理每个任务：打开页面 → 按步骤点击/输入 → 根据「成功指标」判断是否领取成功。
3. **冷却**：成功后将水龙头名称与时间写入 `claim_history.json`，同一水龙头 24 小时内不再执行。
4. **定时**：`scheduler.py` 按设定时间（如每天一次）调用上述流程。

---

## 三、环境与依赖

- Python 3.8+
- 已安装 Chromium（Crawl4AI 会使用 Playwright 自带的浏览器）

```bash
pip install -r requirements.txt
# 首次使用如需安装 Playwright 浏览器：
# playwright install chromium
```

---

## 四、配置说明

### 1. 钱包与代理（config.py）

```python
# 接收测试币的钱包地址
WALLET_ADDRESS = "0x1b085cB185CE7340731D641AEA498F49c5F6d85b"

# 可选：代理，防止 IP 限流（如 http://user:pass@host:port）
PROXY = os.getenv("PROXY_URL")
```

### 2. 水龙头任务结构（FAUCET_TASKS）

每个任务是一个字典，包含：

| 字段 | 含义 |
|------|------|
| `name` | 任务名称，用于日志和冷却记录 |
| `url` | 水龙头页面地址 |
| `network` | 网络名称（如 "Ethereum Sepolia"），仅作记录 |
| `steps` | 操作步骤列表（见下） |
| `success_indicators` | 成功判断条件（见下） |

### 3. 步骤类型（steps）

| action | 说明 | 常用参数 |
|--------|------|----------|
| `type` | 在输入框输入内容 | `selector`, `value`（可含 `WALLET_ADDRESS`） |
| `click` | 点击元素 | `selector`（支持 `button:has-text('Claim')` 等） |
| `select` | 下拉框选择 | `selector`, `value` |
| `wait_for_text` | 等待页面出现某段文字 | `text`, `timeout`（秒） |
| `solve_captcha` | 暂停，等待人工完成验证码后按回车继续 | 无 |

### 4. 成功指标（success_indicators）

用于在步骤执行后判断「是否领取成功」，满足其一即视为成功：

| type | 说明 | 参数 |
|------|------|------|
| `text_in_page` | 页面 HTML 中包含某段文字 | `content` |
| `element_present` | 页面中包含某选择器对应内容 | `selector` |

---

## 五、如何添加新水龙头

1. 在浏览器中手动走一遍流程：打开水龙头 URL → 输入地址 → 选择网络/代币 → 点击领取。
2. 用开发者工具或「检查」确认：输入框、按钮、下拉框的 CSS 选择器或可识别文字。
3. 在 `config.py` 的 `FAUCET_TASKS` 中追加一个对象，例如：

```python
{
    "name": "Sepolia 水龙头",
    "url": "https://sepolia-faucet.pk910.de/",
    "network": "Ethereum Sepolia",
    "steps": [
        {"action": "type", "selector": "input[type='text']", "value": WALLET_ADDRESS,
         "description": "输入钱包地址"},
        {"action": "click", "selector": "button[type='submit']", "description": "点击提交"},
        {"action": "wait_for_text", "text": "funded", "timeout": 30, "description": "等待到账提示"}
    ],
    "success_indicators": [
        {"type": "text_in_page", "content": "successfully funded"},
        {"type": "text_in_page", "content": "Transaction sent"}
    ]
}
```

4. 若页面有验证码，在对应位置插入一步 `{"action": "solve_captcha", "description": "等待手动验证码"}` 即可。

---

## 六、运行方式

### 手动执行一次（调试或单次领取）

```bash
python faucet_claimer.py
```

建议首次将 `faucet_claimer.py` 中 `headless=False`，便于观察浏览器行为。

### 定时自动执行（每日一次）

```bash
python scheduler.py
```

默认每天 10:15 执行；可在 `scheduler.py` 中修改 `schedule.every().day.at("10:15")` 或改为 `schedule.every(24).hours.do(job)` 等。

---

## 七、注意事项

- **选择器与页面变更**：水龙头改版后，选择器或文案可能失效，需重新配置对应任务的 `steps` 和 `success_indicators`。
- **验证码**：遇到验证码时使用 `solve_captcha` 步骤，脚本会暂停直到你在浏览器中完成验证并在终端按回车。
- **频率与封禁**：多数水龙头有频率或 IP 限制，本方案已做 24 小时冷却和任务间间隔；必要时配置 `PROXY` 或减少并发/频率。
- **历史记录**：`claim_history.json` 记录每个水龙头上次成功领取时间，删除该文件可重置冷却（慎用）。

---

## 八、文件说明

| 文件 | 作用 |
|------|------|
| `config.py` | 钱包地址、代理、水龙头任务列表 |
| `faucet_claimer.py` | 浏览器自动化执行与成功判断、冷却逻辑 |
| `scheduler.py` | 定时触发 `faucet_claimer` |
| `claim_history.json` | 自动生成，记录各水龙头上次领取时间 |
| `requirements.txt` | Python 依赖 |

按上述配置好钱包和任务后，可直接运行 `faucet_claimer.py` 或 `scheduler.py` 完成从 Faucet 获取区块链测试币的自动化方案。
