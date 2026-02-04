# 爬取入口：可填单个视频页或课程页，会从该页解析出本课程下全部视频链接
ENTRY_URL = "https://learnblockchain.cn/course/28"
COURSE_ID = 28

# 视频与元数据保存目录（相对本文件所在目录）
OUTPUT_DIR = "downloads"

# 爬虫行为
HEADLESS = True
PAGE_LOAD_WAIT_MS = 8000  # 页面加载后等待时间（毫秒），便于 JS 渲染播放器
