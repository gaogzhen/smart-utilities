import browser_cookie3
import requests

cookies = browser_cookie3.chrome(domain_name='bilibili.com')

SESSDATA,bili_jct,buvid3,DedeUserID = cookies

print(SESSDATA)

for v in  cookies:
    print(v.name, '---', v.value)