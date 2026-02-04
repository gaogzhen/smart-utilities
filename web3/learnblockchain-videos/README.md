# LearnBlockchain 课程视频爬取

使用 [Crawl4AI](https://github.com/unclecode/crawl4ai) 爬取 [登链社区](https://learnblockchain.cn) 指定课程下的全部视频链接，并尝试解析真实视频流地址后下载到本地。

## 环境

- Python 3.10+
- 依赖见 `requirements.txt`

## 安装

```bash
cd learnblockchain-videos
pip install -r requirements.txt
# 若尚未安装 Playwright 浏览器，可执行：
crawl4ai-setup
# 或使用项目内浏览器目录时，在项目下执行：
playwright install chromium
```

## 配置

在 `config.py` 中可修改：

- **ENTRY_URL**：爬取入口（单个视频页或课程页均可，会从该页解析出本课程下全部视频链接）
- **COURSE_ID**：课程 ID，用于过滤视频链接（默认 28）
- **OUTPUT_DIR**：视频与元数据保存目录（默认 `downloads`）
- **HEADLESS**：是否无头模式
- **PAGE_LOAD_WAIT_MS**：页面加载后等待时间（毫秒），便于 JS 渲染播放器

## 使用

```bash
python video_crawler.py
```

流程简述：

1. 用 Crawl4AI 打开入口页，从 HTML 中解析出本课程下所有 `/video/play/xxx?course_id=xx` 链接及标题。
2. 将视频列表保存为 `downloads/videos_list.json`。
3. 逐个打开每个视频播放页，尝试从页面中解析出真实视频流地址（`video` 标签、`data-src`、脚本中的 m3u8/mp4 等）。
4. 对解析到流地址的视频进行下载（m3u8 会尝试简单合并为 ts，复杂 m3u8 可保存索引后用 ffmpeg/yt-dlp 处理）。

**说明**：登链部分视频需登录后可观看高清/完整内容，未登录时可能无法解析到流地址，脚本会保留 `videos_list.json` 供手动或登录后再试。

## 输出

- `downloads/videos_list.json`：视频列表（含标题、URL、解析到的 `video_src`）。
- `downloads/*.mp4` 或 `downloads/*.ts`：成功解析并下载的视频文件。
