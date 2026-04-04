import asyncio
import time
import random

import browser_cookie3
from bilibili_api import Credential, user,favorite_list,comment
from bilibili_api.comment import CommentResourceType
from bilibili_api import request_settings

from common import get_credential

# 防防控1：代理池。没有代理池不考虑并行执行
# proxies = [
#     'http://120.26.0.11:8880',
#     'http://39.101.132.59:8443',
#     'http://222.213.85.99:9002',
#     'http://139.196.46.164:8888'
# ]
exclude_folders = ['默认收藏夹', '饭菜', '思考','娱乐',
                   '产品', '移动开发', 'web3', 'gis', '运维', '云计算', 'go', '中间件',
                   '数据库', '人工智能']
text = '欢迎小伙伴一起学习交流，有做笔记和代码练习，一起加油啊[脱单doge][脱单doge][脱单doge]'

async def main() -> None:
    # 获取用户信息
    credential = get_credential()
    my_info = await user.get_self_info(credential)
    my_mid = my_info['mid']

    # 获取视频收藏夹
    folders = await favorite_list.get_video_favorite_list(uid=my_mid, credential=credential)
    for folder in folders['list']:
        # 清理收藏的失效视频
        await favorite_list.clean_video_favorite_list_content(media_id=folder.get('id'), credential=credential)
        # 过滤掉名单中收藏夹
        if folder and folder.get('title') not in exclude_folders:
            i = 1
            while True:
                videos = await favorite_list.get_video_favorite_list_content(media_id=folder.get('id'),credential=credential, page=i)
                # request_settings.set_proxy(random.choice(proxies))
                for idx, media in enumerate(videos.get('medias'), start=1):
                    # 发表评论
                    try:
                        await comment.send_comment(text=text, oid=media.get('id'), type_= CommentResourceType.VIDEO,
                                               credential=credential)
                        print(f'{folder.get('title')}:{ (i-1)*20 + idx}: {media.get("title")} == success')
                        # 防风控2：随机延迟时间
                        time.sleep(random.uniform(5, 10))
                    except Exception as e:
                        print(e)

                # 是否还有下一页
                if not videos.get('has_more'):
                    break
                i = i + 1



if __name__ == '__main__':
    asyncio.run(main())
