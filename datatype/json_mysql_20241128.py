# -*- encoding: utf-8 -*-
import os
import json

import MySQLUtil as util


def replace_expert_declare():
    # link = util.MySQLUtil(host="自己的ip或者域名", user='自己的用户名', passwd='自己的密码', db='自己的数据库')
    link = util.MySQLUtil(host="localhost", user='root', passwd='mysql@G2ZH', db='sports_competition')
    #link = util.MySQLUtil(host="172.17.69.14", user='root', passwd='Tiyuchanye.pw', db='sports_competition')
    # print(link.list_tables())
    declare_records = link.execute('select * from competition_declare_record where item_id=135')
    print(len(declare_records))
    for declare_record in declare_records:
        declare_datas_str = declare_record[14]
        # print(declare_datas_str)
        if os.path.isfile(declare_datas_str):
            # datas = ''
            with open(declare_datas_str) as f:
                declare_datas = json.load(f)
                # print(declare_datas)
                up_project = declare_datas[3]
                # print(up_project)
                configFormList = up_project['configFormList']
                declareDetails = up_project['declareDetails']
                declareDetails_list = json.loads(declareDetails)
                # print(type(declareDetails_list))
                # print(type(configFormList))
                for index,item in enumerate(declareDetails_list):
                    # print(index, ' ', item)
                    if item['tableItemName'] == '上届赛事转播情况':
                        if item['tableItemType'] == 'checkbox':
                            up_competition = configFormList[index]
                            up_competition_value = up_competition['value']
                            if len(up_competition_value) == 0:
                                continue
                            up_competition['value'] = [i for i in up_competition_value if type(i) == int]
                            # print(index, up_competition['value'])
                        elif item['tableItemType'] == 'fileUpload':
                            # print(index, item)
                            declareDetails_list[index]['tableItemName'] = '上届赛事转播情况附件'
                            up_competition_file = configFormList[index]
                            # print(up_competition_file)
                            # print(up_competition_file['field'], '===', up_competition_file['title'])
                            up_competition_file['field'] = 'sjsszbqkfj'
                            up_competition_file['title'] = '上届赛事转播情况附件'
                            if 'value' in up_competition_file:
                                # print(up_competition_file['value'])
                                up_competition_file['value'] = [i for i in up_competition_file['value'] if type(i) == str]
                                # print(up_competition_file['value'])
                            # print(up_competition_file)
                up_project['declareDetails'] = json.dumps(declareDetails_list, ensure_ascii=False, separators=(',', ':'))
                # print(up_project['declareDetails'])
                with open(declare_datas_str + '_new', 'w') as f1:
                    json.dump(declare_datas, f1, ensure_ascii=False, separators=(',', ':'))
            os.remove(declare_datas_str)

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
    replace_file(dir)