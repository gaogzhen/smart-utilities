import os
import json

import MySQLUtil as util


expert_declare_data_str = '{"type":"radio","field":"zjjl","title":"专家结论","value":"1","prefix":{"type":"div","style":"color:#97a8be;font-size: 12px;line-height:20px; ","children":[]},"placeholder":null,"suffix":null,"props":{"type":null,"placeholder":null,"disabled":false,"uploadType":null,"action":null,"multiple":true,"onSuccess":null},"validate":[{"required":true,"type":"string","message":"专家结论不能为空"}],"options":[{"value":"1","label":"通过","disabled":false},{"value":"2","label":"不通过","disabled":false}],"col":{"span":24},"on":{},"children":[],"effect":{},"hidden":false,"display":true}'
expert_comment_data_str = '{"type":"input","field":"ly","title":"理由","value":"","prefix":{"type":"div","style":"color:#97a8be;font-size: 12px;line-height:20px; ","children":["通过/不同意见"]},"placeholder":"通过/不同意见","suffix":null,"props":{"type":"text","placeholder":null,"disabled":false,"uploadType":null,"action":null,"multiple":true,"onSuccess":null},"validate":null,"options":[],"col":{"span":24},"on":{},"children":[],"effect":{},"hidden":false,"display":true}'

expert_declare_data = json.loads(expert_declare_data_str)
expert_comment_data = json.loads(expert_comment_data_str)


def replace_expert_score():
    link = util.MySQLUtil(host="自己的ip或者域名", user='自己的用户名', passwd='自己的密码', db='自己的数据库')
    # print(link.list_tables())
    score_records = link.execute('select * from competition_expert_score_record')
    for score_record in score_records:
        declare_datas_str = score_record[4]
        id = score_record[0]
        record_id = score_record[1]
        # print(declare_datas_str)
        if not declare_datas_str.startswith('/'):
            # print(declare_datas)
            declare_datas = json.loads(declare_datas_str)
            declare_data = declare_datas[0]
            # print(declare_data)
            scoreDetails = declare_data['expertScoreFormList']
            # print(type(scoreDetails_str))
            # scoreDetails = json.loads(scoreDetails_str)
            if len(scoreDetails) != 0:
                for idx, scoreDetail in enumerate(scoreDetails):
                    if scoreDetail['title'] == '专家评语':
                        # 有替换+新增
                        scoreDetails[idx] = expert_declare_data
                        scoreDetails.append(expert_comment_data)
                        # print(scoreDetails)
                        # print(declare_datas)
                        # scoreDetails_str = json.dumps(scoreDetails, separators=(',', ':'))
                        # print(scoreDetails_str)
                        declare_data['expertScoreFormList'] = scoreDetails
                        declare_datas[0] = declare_data
                        # print(declare_datas)
                        datas = json.dumps(declare_datas, ensure_ascii=False, separators=(',', ':'))
                        # print(datas)
                        sql = "update  competition_expert_score_record set  score_info='" + datas + "' where id=" + str(id)
                        print(sql)
                        # result = link.execute(sql)
                        result = link.update(sql)
                        print(result)
                        print('*===*'*10)
                        # 如果专家评语值为1 总分减去1
                        if scoreDetail['value'] == '1':
                            update_expert_score = "update competition_expert_score_record set expert_score=expert_score-1 where id="+str(id)
                            print(update_expert_score)
                            ret_expert_score = link.update(update_expert_score)
                            print(ret_expert_score)
                            update_declare_score = "update competition_declare_record set expert_score=expert_score-1 where id=" + str(record_id)
                            print(update_declare_score)
                            ret_declare_score = link.update(update_declare_score)
                            print(ret_declare_score)
                            print('*===*' * 10)
                        break
                else:
                    # 没有新增
                    # last_score_detail = scoreDetails[-1]
                    scoreDetails.append(expert_declare_data)
                    scoreDetails.append(expert_comment_data)
                    # print(scoreDetails)
                    # print(declare_datas)
                    # scoreDetails_str = json.dumps(scoreDetails, ensure_ascii=False, separators=(',', ':'))
                    # print(scoreDetails_str)
                    declare_data['expertScoreFormList'] = scoreDetails
                    declare_datas[0] = declare_data
                    # print(declare_datas)
                    datas = json.dumps(declare_datas, ensure_ascii=False, separators=(',', ':'))
                    # print(datas)
                    sql = "update  competition_expert_score_record set  score_info='" + datas + "' where id=" + str(id)
                    print(sql)
                    # result = link.execute(sql)
                    result = link.update(sql)
                    print(result)
                    print('*===*' * 10)
        else:
            list_dir = [declare_datas_str]
            for item in list_dir:
                file_path = item
                if os.path.isfile(file_path):
                    datas = ''
                    with open(file_path) as f:
                        declare_datas = json.load(f)
                        # print(declare_datas)
                        declare_data = declare_datas[0]
                        # print(declare_data)
                        scoreDetails = declare_data['expertScoreFormList']
                        if len(scoreDetails) != 0 :
                            for idx, scoreDetail in enumerate(scoreDetails):
                                if len(scoreDetails) != 0:
                                    if scoreDetail['title'] == '专家评语':
                                        # 有替换+新增
                                        scoreDetails[idx] = expert_declare_data
                                        scoreDetails.append(expert_comment_data)
                                        # print(scoreDetails)
                                        # print(scoreDetails)
                                        # print(declare_datas)
                                        # scoreDetails_str = json.dumps(scoreDetails, ensure_ascii=False, separators=(',', ':'))
                                        # print(scoreDetails_str)
                                        declare_data['expertScoreFormList'] = scoreDetails
                                        declare_datas[0] = declare_data
                                        # print(declare_datas)
                                        datas = declare_datas
                                        with open(file_path + '_new', 'w') as f:
                                            json.dump(datas, f, ensure_ascii=False, separators=(',', ':'))
                                        print('*===*' * 10)
                                        # 如果专家评语值为1 总分减去1
                                        if scoreDetail['value'] == '1':
                                            update_expert_score = "update competition_expert_score_record set expert_score=expert_score-1 where id=" + str(id)
                                            print(update_expert_score)
                                            ret_expert_score = link.update(update_expert_score)
                                            print(ret_expert_score)
                                            update_declare_score = "update competition_declare_record set expert_score=expert_score-1 where id=" + str(record_id)
                                            print(update_declare_score)
                                            ret_declare_score = link.update(update_declare_score)
                                            print(ret_declare_score)
                                            print('*===*' * 10)
                                        break
                            else:
                                # 没有新增
                                scoreDetails.append(expert_declare_data)
                                scoreDetails.append(expert_comment_data)
                                # print(scoreDetails)
                                # print(declare_datas)
                                # print(scoreDetails_str)
                                declare_data['expertScoreFormList'] = scoreDetails
                                declare_datas[0] = declare_data
                                # print(declare_datas)
                                datas = declare_datas
                                # print(datas)
                                with open(file_path + '_new', 'w') as f:
                                    json.dump(datas, f, ensure_ascii=False, separators=(',', ':'))
                                print('*===*' * 10)

def replace_file(dir):
    """
    替换文件
    :return:
    """
    list_dir = os.listdir(dir)
    for item in list_dir:
        file_path = dir + item
        if os.path.isfile(file_path) and item.endswith('.json'):
            os.rename(file_path, file_path+'_old')
    for item in list_dir:
        file_path = dir + item
        if os.path.isfile(file_path) and item.endswith('_new'):
            os.rename(file_path, str.replace(file_path, '_new', ''))

if __name__ == '__main__':
    dir = '/home/inspur/competition-admin/expert_file/'
    replace_expert_score()
    replace_file(dir)