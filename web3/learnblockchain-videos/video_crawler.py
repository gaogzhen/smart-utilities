"""
使用 Crawl4AI 爬取 learnblockchain.cn 课程下的全部视频链接与播放页，
并尝试解析真实视频地址后下载到本地。
"""
import os
import re
import json
import asyncio
from pathlib import Path
from urllib.parse import urljoin, urlparse, parse_qs

# 使用系统默认的 Playwright 浏览器路径（运行 playwright install 时的安装位置）
# 若需使用项目内浏览器，可取消下面注释并先执行: PLAYWRIGHT_BROWSERS_PATH=... playwright install
_script_dir = os.path.dirname(os.path.abspath(__file__))
# os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH", os.path.join(_script_dir, ".playwright-browsers"))

from crawl4ai import AsyncWebCrawler
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig
from bs4 import BeautifulSoup
import httpx

from config import ENTRY_URL, COURSE_ID, OUTPUT_DIR, HEADLESS, PAGE_LOAD_WAIT_MS


def extract_video_list(html: str, base_url: str) -> list[dict]:
    """从课程/视频页 HTML 中提取本课程下所有视频链接与标题。仅解析左侧 div.lession_item 下的 a 链接。"""
    soup = BeautifulSoup(html, "html.parser")
    seen = set()
    videos = []
    base_domain = urlparse(base_url).netloc

    # 视频链接位于页面左侧 div.lession_item 下的 a 标签（兼容 lesson_item 拼写）
    def is_lesson_item(classes):
        if not classes:
            return False
        s = " ".join(classes) if isinstance(classes, list) else str(classes)
        return "lesson_item" in s

    for item in soup.find_all("div", class_=is_lesson_item):
        a = item.find("a", href=True)
        if not a:
            continue
        href = a.get("href", "").strip()
        if not href or "video/play" not in href:
            continue
        full_url = urljoin(base_url, href)
        parsed = urlparse(full_url)
        if parsed.netloc != base_domain:
            continue
        qs = parse_qs(parsed.query)
        if str(COURSE_ID) not in qs.get("course_id", []):
            continue
        path = parsed.path or ""
        m = re.search(r"/video/play/(\d+)", path)
        if not m:
            continue
        video_id = m.group(1)
        if video_id in seen:
            continue
        seen.add(video_id)
        title = (a.get_text() or "").strip() or f"video_{video_id}"
        title = re.sub(r"[\s/\\:*?\"<>|]+", "_", title)[:120]
        videos.append({
            "video_id": video_id,
            "title": title,
            "url": full_url,
        })
    return videos


def extract_video_src_from_page(html: str) -> str | None:
    """从单个视频播放页 HTML 中尝试提取视频流地址（m3u8 / mp4 等）。"""
    if not html:
        return None
    # 1) <video src="..."> 或 <video><source src="...">
    soup = BeautifulSoup(html, "html.parser")
    video = soup.find("video")
    if video:
        src = video.get("src")
        if src:
            return src.strip()
        source = video.find("source", src=True)
        if source and source.get("src"):
            return source["src"].strip()

    # 2) 常见 data 属性
    for tag in soup.find_all(attrs={"data-src": True}):
        u = (tag.get("data-src") or "").strip()
        if u and (".m3u8" in u or ".mp4" in u):
            return u
    for tag in soup.find_all(attrs={"data-url": True}):
        u = (tag.get("data-url") or "").strip()
        if u and (".m3u8" in u or ".mp4" in u):
            return u

    # 3) 页面脚本中的 m3u8 / mp4 URL
    for script in soup.find_all("script"):
        text = (script.string or "").strip()
        if not text:
            continue
        m = re.search(r'["\'](https?://[^"\']+\.m3u8[^"\']*)["\']', text)
        if m:
            return m.group(1).strip()
        m = re.search(r'["\'](https?://[^"\']+\.mp4[^"\']*)["\']', text)
        if m:
            return m.group(1).strip()

    return None


def sanitize_filename(name: str) -> str:
    return re.sub(r'[<>:"/\\|?*]', "_", name).strip() or "video"


async def crawl_video_list_and_pages(videos: list[dict], crawler) -> list[dict]:
    """对每个视频页用 crawl4ai 拉取 HTML，并解析出视频流 URL。"""
    run_config = CrawlerRunConfig(
        page_timeout=60000,
        delay_before_return_html=PAGE_LOAD_WAIT_MS / 1000.0,
    )
    for i, v in enumerate(videos):
        url = v["url"]
        print(f"  [{i+1}/{len(videos)}] {v['title'][:50]}...")
        try:
            result = await crawler.arun(url, config=run_config)
            if result and result.success and result.html:
                src = extract_video_src_from_page(result.html)
                v["video_src"] = src
                if src:
                    print(f"       -> 解析到流: {src[:80]}...")
            else:
                v["video_src"] = None
        except Exception as e:
            print(f"       -> 请求失败: {e}")
            v["video_src"] = None
        await asyncio.sleep(1)
    return videos


def download_file(url: str, path: Path, timeout: float = 60.0) -> bool:
    """下载单个文件（如 m3u8 索引或 mp4）到 path。"""
    try:
        with httpx.Client(follow_redirects=True, timeout=timeout) as client:
            r = client.get(url)
            r.raise_for_status()
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(r.content)
            return True
    except Exception as e:
        print(f"      下载失败 {url[:60]}...: {e}")
        return False


def download_m3u8_simple(url: str, out_path: Path, timeout: float = 30.0) -> bool:
    """
    简单 m3u8：仅当索引里是单层且 ts 为绝对 URL 时直接拉取 ts 并合并。
    若为多级或相对路径则只保存 m3u8 索引，后续可用 ffmpeg/yt-dlp 处理。
    """
    try:
        with httpx.Client(follow_redirects=True, timeout=timeout) as client:
            r = client.get(url)
            r.raise_for_status()
            text = r.text
    except Exception as e:
        print(f"      获取 m3u8 失败: {e}")
        return False

    base = url.rsplit("/", 1)[0] + "/"
    lines = text.strip().splitlines()
    ts_urls = []
    for line in lines:
        line = line.strip()
        if line.startswith("#"):
            continue
        if line.endswith(".ts"):
            ts_urls.append(urljoin(base, line))
        elif ".m3u8" in line:
            # 多级 m3u8，只保存主索引
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(text, encoding="utf-8")
            print(f"      多级 m3u8，已保存索引到 {out_path}，可用 ffmpeg/yt-dlp 下载")
            return True

    if not ts_urls:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(text, encoding="utf-8")
        print(f"      已保存 m3u8 索引到 {out_path}")
        return True

    # 简单合并 ts
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "wb") as f:
        for u in ts_urls:
            try:
                rr = httpx.get(u, follow_redirects=True, timeout=timeout)
                rr.raise_for_status()
                f.write(rr.content)
            except Exception as e:
                print(f"      下载 ts 失败 {u[:50]}...: {e}")
    print(f"      已合并保存: {out_path}")
    return True


async def download_videos(videos: list[dict], output_dir: Path) -> None:
    """根据解析到的 video_src 下载到 output_dir。"""
    for v in videos:
        src = v.get("video_src")
        if not src:
            continue
        name = sanitize_filename(v["title"])
        vid = v.get("video_id", "")
        if vid:
            name = f"{vid}_{name}"
        if ".m3u8" in src:
            path = output_dir / f"{name}.ts"
            download_m3u8_simple(src, path)
        else:
            path = output_dir / f"{name}.mp4"
            download_file(src, path)
        await asyncio.sleep(0.5)


async def main():
    output_dir = Path(_script_dir) / OUTPUT_DIR
    output_dir.mkdir(parents=True, exist_ok=True)
    list_file = output_dir / "videos_list.json"

    browser_config = BrowserConfig(headless=HEADLESS)
    run_config = CrawlerRunConfig(
        page_timeout=60000,
        delay_before_return_html=PAGE_LOAD_WAIT_MS / 1000.0,
    )

    print("=== 1. 爬取入口页，解析课程下全部视频链接 ===")
    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(ENTRY_URL, config=run_config)
        if not result or not result.success:
            print("入口页爬取失败，请检查 ENTRY_URL 与网络")
            return
        html = result.html or ""
        base_url = getattr(result, "final_url", None) or getattr(result, "url", None) or ENTRY_URL
        videos = extract_video_list(html, base_url)
        print(f"共解析到 {len(videos)} 个视频")

    if not videos:
        print("未解析到任何视频链接，请确认页面包含 /video/play/...?course_id= 链接")
        return

    with open(list_file, "w", encoding="utf-8") as f:
        json.dump(videos, f, ensure_ascii=False, indent=2)
    print(f"视频列表已保存: {list_file}\n")

    print("=== 2. 逐个打开视频播放页，尝试解析真实视频流地址 ===")
    async with AsyncWebCrawler(config=browser_config) as crawler:
        videos = await crawl_video_list_and_pages(videos, crawler)

    with open(list_file, "w", encoding="utf-8") as f:
        json.dump(videos, f, ensure_ascii=False, indent=2)

    print("\n=== 3. 根据解析结果下载视频 ===")
    await download_videos(videos, output_dir)
    print("\n完成。未解析到流地址的视频可能需登录或反爬，可查看 videos_list.json 手动处理。")


if __name__ == "__main__":
    asyncio.run(main())
