import browser_cookie3
import requests

cookies = list(browser_cookie3.chrome(domain_name='bilibili.com'))
cookie_map = {cookie.name: cookie.value for cookie in cookies}
print(cookie_map['SESSDATA'])
# SESSDATA,bili_jct,buvid3,DedeUserID =
#
# print(SESSDATA)
#
# for v in  cookies:
#     print(v.name, '---', v.value)