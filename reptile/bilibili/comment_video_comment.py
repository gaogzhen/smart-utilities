import asyncio
import time
import random
from datetime import datetime

from bilibili_api import Credential
from bilibili_api.comment import CommentResourceType,get_comments
from bilibili_api.video import Video

from common import get_credential

"""
回复指定视频评论
"""
async def main() -> None:
    # 获取凭证
    credential = get_credential()
    # 获取指定视频信息
    bvid = "BV123yAYMEwb"
    v_ret = Video(bvid, credential)
    info = await v_ret.get_info()
    comments = await v_ret.get_comments()
    print(comments)
# 获取指定视频下评论

# 过滤评论

# 回复评论

if __name__ == '__main__':
    asyncio.run(main())