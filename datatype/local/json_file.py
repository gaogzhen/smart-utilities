import os
import json


def replace_declare(dir):
    """
    生成新文件
    :return:
    """

    list_dir = os.listdir(dir)
    # list_dir  = [].append(dir + '33_131.json')

    # list_dir = ['23_131.json']

    expert_declare_str = '{\"tableItemId\":5,\"tableItemName\":\"专家结论\",\"tableItemType\":\"radio\",\"tableItemTip\":null,\"selectDetails\":[{\"selectItemId\":1,\"selectItemName\":\"通过\"},{\"selectItemId\":2,\"selectItemName\":\"不通过\"}],\"tableItemSort\":60,\"tableItemRequired\":\"1\"}'
    expert_comment_str = '{\"tableItemId\":6,\"tableItemName\":\"理由\",\"tableItemType\":\"input\",\"tableItemTip\":\"通过/不通过意见\",\"selectDetails\":[],\"tableItemSort\":61,\"tableItemRequired\":\"0\"}'
    expert_declare = json.loads(expert_declare_str)
    expert_comment = json.loads(expert_comment_str)

    # print(list_dir)

    for item in list_dir:
        file_path = dir + item
        if os.path.isfile(file_path) and item.endswith('.json'):
            print(file_path)
            datas = ''
            with open(file_path) as f:
                declare_datas = json.load(f)
                # print(declare_datas)
                declare_data = declare_datas[0]
                # print(declare_data)
                scoreDetails_str = declare_data['scoreDetails']

                scoreDetails = json.loads(scoreDetails_str)
                if len(scoreDetails) != 0:
                    for idx, scoreDetail in enumerate(scoreDetails):
                        if scoreDetail['tableItemName'] == '专家评语':
                            # 有替换+新增
                            expert_declare['tableItemId'] = scoreDetail['tableItemId']
                            expert_declare['tableItemSort'] = scoreDetail['tableItemSort']
                            expert_comment['tableItemId'] = scoreDetail['tableItemId'] + 1
                            expert_comment['tableItemSort'] = scoreDetail['tableItemSort'] + 1
                            scoreDetails[idx] = expert_declare
                            scoreDetails.append(expert_comment)

                            scoreDetails_str = json.dumps(scoreDetails, ensure_ascii=False, separators=(',', ':'))
                            # print(scoreDetails_str)
                            declare_data['scoreDetails'] = scoreDetails_str
                            declare_datas[0] = declare_data
                            # print(declare_datas)
                            datas = declare_datas
                            with open(file_path + '_new', 'w') as f:
                                json.dump(datas, f, ensure_ascii=False, separators=(',', ':'))
                            break
                    else:
                        # 没有新增
                        print(scoreDetails)
                        last_score_detail = scoreDetails[-1]
                        expert_declare['tableItemId'] = last_score_detail['tableItemId'] + 1
                        expert_declare['tableItemSort'] = last_score_detail['tableItemSort'] + 1
                        expert_comment['tableItemId'] = last_score_detail['tableItemId'] + 2
                        expert_comment['tableItemSort'] = last_score_detail['tableItemSort'] + 2
                        scoreDetails.append(expert_declare)
                        scoreDetails.append(expert_comment)
                        # print(scoreDetails)
                        # print(declare_datas)
                        scoreDetails_str = json.dumps(scoreDetails, ensure_ascii=False, separators=(',', ':'))
                        # print(scoreDetails_str)
                        declare_data['scoreDetails'] = scoreDetails_str
                        declare_datas[0] = declare_data
                        # print(declare_datas)
                        datas = declare_datas
                        # print(datas)
                        with open(file_path + '_new', 'w') as f:
                            json.dump(datas, f, ensure_ascii=False, separators=(',', ':'))


def replace_file(dir):
    """
    替换文件
    :return:
    """
    list_dir = os.listdir(dir)
    for item in list_dir:
        file_path = dir + item
        if os.path.isfile(file_path) and item.endswith('.json'):
            os.rename(file_path, file_path + '_old')
    for item in list_dir:
        file_path = dir + item
        if os.path.isfile(file_path) and item.endswith('_new'):
            os.rename(file_path, str.replace(file_path, '_new', ''))


if __name__ == '__main__':
    dir = '/Users/gaogzhen/logs/inspur/competition-admin/declare_file/'
    replace_declare(dir)
    replace_file(dir)
