import asyncio
import time

import browser_cookie3
from bilibili_api import Credential, user, comment
from bilibili_api.comment import CommentResourceType


async def main() -> None:
    # 获取用户历史记录
    # 获取cookie
    cookies = browser_cookie3.chrome(domain_name='bilibili.com')

    cre = dict()
    for cookie in cookies:
        if cookie.name == 'SESSDATA' or cookie.name == 'bili_jct' or cookie.name == 'buvid3' or cookie.name == 'DedeUserID':
           cre[cookie.name] = cookie.value
    # 创建凭据
    credential = Credential(sessdata=cre['SESSDATA'], bili_jct=cre['bili_jct'], buvid3=cre['buvid3'], dedeuserid=cre['DedeUserID'])
    # 创建用户
    # me = user.User(uid=17142789, credential=credential);
    info = await user.get_self_history(1, 100, credential)
    # print(len(info))
    # lists = await me.get_self_history()
    text = '欢迎小伙伴一起学习交流，有做笔记和代码练习，头像有联系方式和地址，一起加油啊[脱单doge][脱单doge][脱单doge]'
    for v in info:
        time.sleep(2)
        await comment.send_comment(text=text, oid=(v['aid']), type_=CommentResourceType.VIDEO, credential=credential)


if __name__ == '__main__':
    asyncio.run(main())

