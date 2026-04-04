import asyncio
import time

import browser_cookie3
from bilibili_api import Credential, user, comment
from bilibili_api.comment import CommentResourceType

from common import get_credential


async def main() -> None:
    # 获取用户历史记录
    credential = get_credential()
    info = await user.get_self_history(1, 100, credential)
    # print(len(info))
    # lists = await me.get_self_history()
    text = '欢迎小伙伴一起学习交流，有做笔记和代码练习，一起加油啊[脱单doge][脱单doge][脱单doge]'
    for v in info:
        time.sleep(2)
        await comment.send_comment(text=text, oid=(v['aid']), type_=CommentResourceType.VIDEO, credential=credential)


if __name__ == '__main__':
    asyncio.run(main())

