# -*- encoding: utf-8 -*-
import os
import json
import re

import MySQLUtil as util


rp_define = r',{\"tableItemId\":22,\"tableItemName\":\"赛事等级证明材料附件\",\"tableItemType\":\"fileUpload\",\"tableItemTip\":null,\"selectDetails\":[],\"tableItemSort\":22,\"tableItemRequired\":\"1\"}'
rp_val = r',{"col":{"span":24},"field":"ssdjzmclfj","options":[],"prefix":{"children":[null],"style":"color:#97a8be;font-size: 12px;margin-left: 20px;line-height:20px","type":"div"},"props":{"action":"/competition-admin/common/uploadFiles","disabled":false,"multiple":true,"type":"select","uploadType":"file"},"title":"赛事等级证明材料附件","type":"upload","validate":[{"message":"赛事等级证明材料附件不能为空","required":true,"type":"array"}],"value":[]}'

sp_define = r'{\"tableItemId\":21,\"tableItemName\":\"赛事等级（下拉框）\",\"tableItemType\":\"select\",\"tableItemTip\":null,\"selectDetails\":[{\"selectItemId\":1,\"selectItemName\":\"世界顶级体育组织、职业体育俱乐部联盟等举办，具有全球影响力的赛事\"},{\"selectItemId\":2,\"selectItemName\":\"其他国际性赛事、洲际赛事\"},{\"selectItemId\":3,\"selectItemName\":\"全国性赛事\"},{\"selectItemId\":4,\"selectItemName\":\"省级赛事\"},{\"selectItemId\":5,\"selectItemName\":\"市级赛事\"},{\"selectItemId\":6,\"selectItemName\":\"区（县）级赛事\"}],\"tableItemSort\":21,\"tableItemRequired\":\"1\"}'
sp_val = '(\{"col":\{"span":24\},"field":"ssdj（xlk）","options":\[\{"disabled":false,"label":"世界顶级体育组织、职业体育俱乐部联盟等举办，具有全球影响力的赛事","value":"1"\},\{"disabled":false,"label":"其他国际性赛事、洲际赛事","value":"2"\},\{"disabled":false,"label":"全国性赛事","value":"3"\},\{"disabled":false,"label":"省级赛事","value":"4"\},\{"disabled":false,"label":"市级赛事","value":"5"\},\{"disabled":false,"label":"区（县）级赛事","value":"6"\}\],"prefix":\{"children":\[null\],"style":"color:#97a8be;font-size: 12px;margin-left: 20px;line-height:20px","type":"div"\},"props":\{"disabled":false,"multiple":true\},"title":"赛事等级（下拉框）","type":"select","validate":\[\{"message":"赛事等级（下拉框）不能为空","required":true,"type":"array"\}\],"value":\["\d"\]\})'

def replace_expert_declare():
    # link = util.MySQLUtil(host="自己的ip或者域名", user='自己的用户名', passwd='自己的密码', db='自己的数据库')
    link = util.MySQLUtil(host="localhost", user='root', passwd='mysql@G2ZH', db='sports_competition')
    #link = util.MySQLUtil(host="172.17.69.14", user='root', passwd='Tiyuchanye.pw', db='sports_competition')
    # print(link.list_tables())
    declare_records = link.execute('select * from competition_declare_record where item_id=138')
    # print(len(declare_records))
    for declare_record in declare_records:
        declare_datas_str = declare_record[14]
        # print(declare_datas_str)
        if os.path.isfile(declare_datas_str):
            # datas = ''
            with open(declare_datas_str) as f:
                # 替换声明部分
                line = f.readline()
                list_def = line.split(sp_define)
                # list_def = re.split(sp_define, line)
                # print(len(list_def))
                list_def.insert(1, rp_define)
                list_def.insert(1, sp_define)
                # for ret in list_def:
                #     print(ret)
                line = ''.join(list_def)
                # print(line)
                # 替换取值部分
                list_def = re.split(sp_val, line)
                # print(len(list_def))
                list_def.insert(2, rp_val)
                # for ret in list_def:
                #     print(ret)
                line = ''.join(list_def)
                print(line)
                # 生成新文件
                with open(declare_datas_str + '_new', 'w') as f1:
                    f1.write(line)
                    # json.dump(line, f1, ensure_ascii=False, separators=(',', ':'))
            # os.remove(declare_datas_str)

def replace_file(dir):
    """
    替换文件
    :return:
    """
    list_dir = os.listdir(dir)
    # for item in list_dir:
    #     declare_record = dir + item
    #     if os.path.isfile(declare_record) and item.endswith('.json'):
    #         os.rename(declare_record, declare_record+'_old')
    for item in list_dir:
        declare_record = dir + item
        if os.path.isfile(declare_record) and item.endswith('_new'):
            os.rename(declare_record, str.replace(declare_record, '_new', ''))

if __name__ == '__main__':
    # dir = '//inspur/competition-admin/expert_file/'
    dir = '/Users/gaogzhen/logs/inspur/competition-admin/declare_file/'
    # dir = '/data/files/inspur/competition-admin/declare_file/'
    replace_expert_declare()
    # replace_file(dir)