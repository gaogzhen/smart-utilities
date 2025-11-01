import os

import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows

import database.mysql.MySQLUtil as mysql_util
import datatype.type_text_map as type_text_map
import util.str_util as str_util


def dict2xls(path, datas, order, order_map):
    """
    字典/对象数据转为xls
    :param order_map:
    :param order:
    :param path:
    :param datas:
    :return:
    """
    pf = pd.DataFrame(datas)
    pf = pf[order]
    pf.rename(columns=order_map, inplace=True)
    wb = Workbook()
    ws = wb.active
    for r in dataframe_to_rows(pf, index=False, header=True):
        ws.append(r)
    wb.save(path)


def column2xls(link):
    """
    mysql表结构转xls说明文档
    :return:
    """

    column_names = ['column_name', 'column_type', 'attr', 'data_type', 'column_default', 'column_comment']
    column_names_map = {
        "column_name": '表字段名',
        'column_type': '表字段类型',
        'attr': '属性名',
        'data_type': '数据类型',
        'column_default': '默认值',
        'column_comment': '注释'
    }
    sql_table = "select table_name from tables where table_schema='sports_industry'"
    tables = link.query_all(sql_table)
    for table in tables:
        ret = []
        # print(table[0])
        sql_column = "select column_name,column_type,column_default,column_comment,data_type from columns where table_schema='sports_industry' and  table_name='" + \
                     table[0] + "'"
        columns = link.query_all(sql_column)
        for column in columns:
            column_list = list(column)
            column_list.insert(2, str_util.name_convert(column_list[0]))
            column_list.insert(3, type_text_map.mysql_text_map.get(column_list[-1]))
            column_list = column_list[0:-1]
            column_obj = {}
            for column_name, column_val in zip(column_names, column_list):
                column_obj[column_name] = column_val
            # print(column_obj)
            ret.append(column_obj)

        dict2xls(os.getcwd() + '/xls/' + table[0] + '.xlsx', ret, column_names, column_names_map)


if __name__ == '__main__':
    link = mysql_util.MySQLUtil(host="node2231", user='root', passwd='mysql@G2ZH', db='information_schema')
    column2xls(link)
