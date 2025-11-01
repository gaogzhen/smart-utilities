# -*- encoding: utf-8 -*-
import os
import json

import MySQLUtil as util

tp_0 = {
    '填表单位': 'filling_unit',
    '填表人': 'filling_name',
    '联系电话(手机）': 'phone',
    '赛事名称': 'events_name',
    '赛事主办方': 'events_sponsor',
    '赛事主办方（下拉框）': 'events_sponsor_type',
    '赛事承办方': 'events_organizers',
    '赛事协办方': 'events_co_organizer',
    '比赛项目（按实际情况全部罗列）': 'events_item',
    '预计办赛形式（下拉框）': 'events_form',
    '举办日期（开始时间）': 'events_start_time',
    '举办日期（结束时间）': 'events_end_time',
    '赛事举办天数/天': 'events_days',
    '举办地点（市）': 'events_city',
    '举办地点（区县）': 'events_county',
    '举办地点(场地/场馆）': 'events_venue',
    '是否占用公共资源（下拉框）': 'is_occupied_public_resources',
    '占用公共资源附件': 'occupied_public_resources_url',
    '是否纳入国家体育总局赛事计划（下拉框）': 'is_include_nation_events',
    '纳入国家体育总局赛事计划附件': 'include_nation_events_url',
    '赛事等级（下拉框）': 'events_level'
}

# 1赛后竞赛组织情况 after_game_gather_info_ps1 
tp_1= {
    "赛事现场观众人数（县/区内本地人数）": "county_in_live_audience", # 赛事现场观众人数(县/区内本地人数)
    "赛事现场观众人数（县/区以外人数）": "county_out_live_audience", # 赛事现场观众人数(县/区以外人数)
    "赛事现场观众人数（总计人数）": "total_live_audience", # 赛事现场观众人数(总计人数)
    "参赛人数（县/区内本地人数）": "county_in_entrants", # 参赛人数(县/区内本地人数)
    "参赛人数（县/区以外人数）": "county_out_entrants", # 参赛人数(县/区外本地人数)
    "参赛人数（总计人数）": "total_entrants", # 参赛人数(总计人数)
    "志愿者（县/区内本地人数）": "county_in_volunteer", # 志愿者(县/区内本地人数)
    "志愿者（县/区以外人数）": "county_out_volunteer", # 志愿者(县/区以外人数)
    "志愿者（总计人数）": "total_volunteer", # 志愿者(总计人数)
    "办赛组织人员（县/区内本地人数）": "county_in_organizational", # 办赛组织人员岗位分配(县/区内本地人数)
    "办赛组织人员（县/区以外人数）": "county_out_organizational", # 办赛组织人员岗位分配(县/区以外人数)
    "办赛组织人员（总计人数）": "total_organizational", # 办赛组织人员岗位分配(总计人数)
    "裁判员情况（县/区内本地人数）": "county_in_umpire", # 裁判员情况(县/区内本地人数)
    "裁判员情况（县/区以外人数）": "county_out_umpire", # 裁判员情况(县/区以外人数)
    "裁判员情况（总计人数）": "total_umpire", # 裁判员情况(总计人数)
    "现场媒体人数（县/区内本地人数）": "county_in_media_people", # 现场媒体人数(县/区内本地人数)
    "现场媒体人数（县/区以外人数）": "county_out_media_people", # 现场媒体人数(县/区以外人数)
    "现场媒体人数（总计人数）": "total_media_people", # 现场媒体人数(总计人数)
    "赛事已举办届数": "events_held_sessions", # 赛事已举办届数
    "承办方运营届数（此处年限不得大于赛事举办届数）": "organizers_operation_sessions" # 承办方运营届数（此处年限不得大于赛事举办届数）
}

# after_game_gather_info_ps2 = {
tp_2 = {
    "电视平台宣传情况类别1（下拉框）": "tv_platform_category", # 平台宣传情况类别
    "电视平台宣传情况名称1": "tv_platform_name", # 平台宣传情况名称
    "电视平台宣传情况类型1（下拉框）": "tv_platform_type", # 平台宣传情况类型
    "电视平台宣传情况日期1": "tv_platform_time", # 平台宣传情况日期
    "电视平台宣传情况时长/秒1": "tv_platform_duration", # 平台宣传情况时长/秒
    "电视平台宣传情况类别2（下拉框）": "tv_platform_category", # 平台宣传情况类别
    "电视平台宣传情况名称2": "tv_platform_name", # 平台宣传情况名称
    "电视平台宣传情况类型2（下拉框）": "tv_platform_type", # 平台宣传情况类型
    "电视平台宣传情况日期2": "tv_platform_time", # 平台宣传情况日期
    "电视平台宣传情况时长/秒2": "tv_platform_duration", # 平台宣传情况时长/秒
    "电视平台宣传情况类别3（下拉框）": "tv_platform_category", # 平台宣传情况类别
    "电视平台宣传情况名称3": "tv_platform_name", # 平台宣传情况名称
    "电视平台宣传情况类型3（下拉框）": "tv_platform_type", # 平台宣传情况类型
    "电视平台宣传情况日期3": "tv_platform_time", # 平台宣传情况日期
    "电视平台宣传情况时长/秒3": "tv_platform_duration", # 平台宣传情况时长/秒
    "电视平台宣传情况类别4（下拉框）": "tv_platform_category", # 平台宣传情况类别
    "电视平台宣传情况名称4": "tv_platform_name", # 平台宣传情况名称
    "电视平台宣传情况类型4（下拉框）": "tv_platform_type", # 平台宣传情况类型 
    "电视平台宣传情况日期4": "tv_platform_time", # 平台宣传情况日期
    "电视平台宣传情况时长/秒4": "tv_platform_duration", # 平台宣传情况时长/秒
    "电视平台宣传情况类别5（下拉框）": "tv_platform_category", # 平台宣传情况类别
    "电视平台宣传情况名称5": "tv_platform_name", # 平台宣传情况名称
    "电视平台宣传情况类型5（下拉框）": "tv_platform_type", # 平台宣传情况类型
    "电视平台宣传情况日期5": "tv_platform_time", # 平台宣传情况日期
    "电视平台宣传情况时长/秒5": "tv_platform_duration", # 平台宣传情况时长/秒
    "网络视频平台直播情况类别1（下拉框）": "tv_platform_category", # 平台宣传情况类别
    "网络视频平台直播情况名称1": "tv_platform_name", # 平台宣传情况名称
    "网络视频平台直播情况日期1": "tv_platform_time", # 平台宣传情况日期
    "网络视频平台直播情况时长/秒1": "tv_platform_duration", # 平台宣传情况时长/秒
    "网络视频平台直播情况类别2（下拉框）": "tv_platform_category", # 平台宣传情况类别
    "网络视频平台直播情况名称2": "tv_platform_name", # 平台宣传情况名称
    "网络视频平台直播情况日期2": "tv_platform_time", # 平台宣传情况日期
    "网络视频平台直播情况时长/秒2": "tv_platform_duration", # 平台宣传情况时长/秒
    "网络视频平台直播情况类别3（下拉框）": "tv_platform_category", # 平台宣传情况类别
    "网络视频平台直播情况名称3": "tv_platform_name", # 平台宣传情况名称
    "网络视频平台直播情况日期3": "tv_platform_time", # 平台宣传情况日期
    "网络视频平台直播情况时长/秒3": "tv_platform_duration", # 平台宣传情况时长/秒
    "网络视频平台直播情况类别4（下拉框）": "tv_platform_category", # 平台宣传情况类别
    "网络视频平台直播情况名称4": "tv_platform_name", # 平台宣传情况名称
    "网络视频平台直播情况日期4": "tv_platform_time", # 平台宣传情况日期
    "网络视频平台直播情况时长/秒4": "tv_platform_duration", # 平台宣传情况时长/秒
    "网络视频平台直播情况类别5（下拉框）": "tv_platform_category", # 平台宣传情况类别
    "网络视频平台直播情况名称4": "tv_platform_name", # 平台宣传情况名称
    "网络视频平台直播情况日期5": "tv_platform_time", # 平台宣传情况日期
    "网络视频平台直播情况时长/秒5": "tv_platform_duration", # 平台宣传情况时长/秒
}

#数据库"多出来"的字段:"年份","赛事名称","申报id","申报名称","赛事id".
#数据库"缺少"的字段:"证明材料上传至百度云（证明材料名与题目保持一致）"
#3赛后赛事保障情况 after_game_gather_info_ps3 = {
tp_3 = {
    "是否有赛事组织方案": "is_events_scheme", # 是否有赛事组织方案
    "赛事组织方案附件": "events_scheme_url", # 赛事组织方案文件
    "是否有安全保障实施方案": "is_secure_scheme", # 是否有安全保障实施方案
    "安全保障实施方案附件": "secure_scheme_url", # 安全保障实施方案文件
    "是否有风险防控评估报告（第三方出具）": "is_risk_control_report", # 是否有风险防控评估报告（第三方出具）
    "风险防控评估报告（第三方出具）附件": "risk_control_report_url", # 风险防控评估报告文件
    "是否有风险防范方案": "is_risk_control_scheme", # 是否有风险防范方案
    "风险防范方案附件": "risk_control_scheme_url", # 风险防范方案文件
    "是否有医务保障实施方案": "is_medical_coverage_scheme", # 是否有医务保障实施方案
    "医务保障实施方案附件": "medical_coverage_scheme_url", # 医务保障实施方案文件
    "是否有应急处置方案": "is_emergency_scheme", # 是否有应急处置方案
    "应急处置方案附件": "emergency_scheme_url", # 应急处置方案文件
    "证明材料上传至百度云（证明材料名与题目保持一致）": "" #
}

#4赛后赛事收支情况 after_game_gather_info_ps4 = {
tp_4 = {
    "赛事报名费(元/人)": "events_enroll_fee", # 赛事报名费
    "赛事门票费(元/人)": "events_tickets_fee", # 赛事门票费
    "赛事总收入(万元)": "events_revenue", # 赛事总收入
    "政府投入(万元)": "events_invest_administration", # 赛事总投入(政府投入) 
    "社会资金投入(万元)": "events_invest_community", # 赛事总投入(社会资金投入) 
    "赛场搭建": "events_build_fee", # 赛场搭建
    "设备购置及安装费": "equipment_fee", # 设备购置及安装费
    "建设投资的其他投入金额": "other_build_fee_detail", # 其他建设费用用途
    "其他投入金额的具体内容": "other_build_fee", #  其他建设费用（注明具体内容） 
    "建设投资": "build_invest_fee", # 建设投资 (总投资)
    "场地使用费": "venue_fee", # 场地使用费
    "宣传推广费": "advertise_fee", # 宣传推广费
    "赛事服务费": "events_serve_fee", # 赛事服务费
    "赛事奖金": "events_bonus_fee", # 赛事奖金
    "赛事安保服务采购费": "events_security_fee", # 赛事安保服务采购费
    "赛事医疗服务采购费": "events_medical_coverage_fee", # 赛事医疗服务采购费
    "市场开发费": "market_fee", # 市场开发费
    "赛事直播转播费": "events_broadcast_fee", # 赛事直播转播费
    "赛事信息传输、计算机服务和软件服务费": "events_message_fee", # 赛事信息传输、计算机服务和软件服务费
    "赛事酒店住宿费": "events_residential_fee", # 赛事酒店住宿费
    "赛事餐饮费": "events_dining_fee", # 赛事餐饮费
    "赛事交通服务支出费": "events_traffic_fee", # 赛事交通服务支出费
    "服务费用的其他投入金额": "other_serve_fee", # 其他服务费用（注明具体内容）
    "其他投入金额的具体内容": "other_serve_fee_detail", # 其他服务费用用途
    "服务费用": "serve_fee", # 服务费用 (总费用)
    "其他费用": "other_fee", # 其他费用
    "其他费用的具体内容": "other_fee_detail", # 其他费用用途
    "赛事投入合计": "total_fee" # 合计
}


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
                    print(111)
                # print(up_project['declareDetails'])

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
    # dir = '#inspur/competition-admin/expert_file/'
    dir = '/Users/gaogzhen/logs/inspur/competition-admin/declare_file/'
    # dir = '/data/files/inspur/competition-admin/declare_file/'
    replace_expert_declare()