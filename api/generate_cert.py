# import request
import json
import time

import requests

url_complete = 'http://www.eventpack.cn/dxs/back/dxsMember/createComplete'
url_cert = 'http://www.eventpack.cn/dxs/back/dxsMember/createCert'
headers= {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
    'token': 'b601d57331a3b1f5967437feb6d5ff5a9b261bba533ccde78e7f4566a719b798',
    'Content-Type': 'application/json'}
file = open('id.txt', 'r')
text_lines = file.readlines()
# print(type(text_lines), text_lines)
i = 1
for line in text_lines:
    id = int(line.strip('\n'))
    data = {'id': id, 'reload': 1}
    reponse = requests.post(url_complete, headers=headers, data=json.dumps(data))
    print(i , ' ', reponse.text)
    response = requests.post(url_cert, headers=headers, data=json.dumps(data))
    print(i, '', reponse.text)
    i = i + 1
    time.sleep(0.1)
# data={'id': ,'reload': 1}
# headers= {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}
# requests.post(url,headers = headers,data=data)
