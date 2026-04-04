
import os
import browser_cookie3
from bilibili_api import Credential


def get_credential():
    # 获取cookie
    cookies = browser_cookie3.chrome(domain_name='bilibili.com')

    cre = dict()
    for cookie in cookies:
        if cookie.name == 'SESSDATA' or cookie.name == 'bili_jct' or cookie.name == 'buvid3' or cookie.name == 'DedeUserID':
            cre[cookie.name] = cookie.value
    if not cre['SESSDATA'] or not cre['bili_jct'] or not cre['buvid3'] or not cre['DedeUserID']:
        raise Exception("缺少必要的身份凭证信息")
    # 创建凭据
    return  Credential(sessdata=cre['SESSDATA'], bili_jct=cre['bili_jct'], buvid3=cre['buvid3'],
                            dedeuserid=cre['DedeUserID'])
