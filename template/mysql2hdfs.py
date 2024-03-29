# 通过datax把mysql中数据全量同步到hdfs，一个表对应一个同步文件。通过模版文件生成job
import os
import pathlib
import subprocess
from string import Template
from time import sleep

import MySQLUtil as util

# mysql与hdfs数据类型对应map
type_mysql_hdfs = {
    'tinyint': 'tinyint',
    'smallint': 'smallint',
    'int': 'int',
    'bigint': 'bigint',
    'float': 'float',
    'double': 'double',
    'varchar': 'string',
    'bool': 'boolean',
    'timestamp': 'timestamp',
    'datetime': 'string',
    'date': 'date',
    'decimal': 'double',
    'text': 'string'
}


# 读取mysql数据，生成datax gmall
def tmp2job(db_util, tmp_file):
    # 获取模版文件
    tmp_file = pathlib.Path(__file__).parent.joinpath(tmp_file)
    # 生成文件路径
    target_dir = pathlib.Path(__file__).parent.joinpath('gmall')
    # 获取全部表名
    db_util.select_db("gmall")
    tables = db_util.list_tables()
    # tables= [tables[0]]
    for table in tables:
        if table == 'z_log':
            continue
        target_file = target_dir.joinpath(table + '.json')
        with open(tmp_file, mode="r", encoding="utf-8") as r_f, open(
                target_file, mode="w", encoding="utf8"
        ) as w_f:
            template_content = r_f.read()
            # print(f"template_content:{template_content}")
            template = Template(template_content)
            columns = db_util.table_metadata(db='gmall', table=table)
            column_str = ''
            # 拼接hdfswriter column
            for column in columns:
                # print(column)
                type1 = type_mysql_hdfs.get(column[1])
                # print(type1)
                column_str += '{\"name\":\"' + column[0] + '\",\"type\":\"' + type1 + '\"},'
            column_str = column_str[:-1]
            # print(os.path.split(table)[0])
            # 替换模板中的文件名，hdfswriter中的column，及hdfs文件存储路径
            data = template.substitute(table_name=table, COLUMN=column_str, DIRNAME=os.path.splitext(table)[0])
            w_f.write(data)


# 执行job脚本
def execute_shell(db_util):
    # cmd_ls = 'ls /export/server/datax/job/gmall'
    # name = subprocess.check_output(cmd_ls, shell=True)
    # names = str(name, encoding='utf-8').split('\n')[:-1]
    db_util.select_db("gmall")
    names = db_util.list_tables()
    # tables= [tables[0]]
    for name in names:
        if name == 'z_log':
            continue
        # 确保hdfs父路径存在
        hdfs_mkdir = 'hdfs dfs -mkdir -p /origin_data/gmall/db/' + os.path.splitext(name)[0]
        print('-'*5, hdfs_mkdir,'-'*5,name)
        ret = subprocess.check_call(hdfs_mkdir, shell=True)
        print('---ret--',ret)
        # 执行datax job任务
        commond = "python /export/server/datax/bin/datax.py  /export/server/datax/job/gmall/" + name + '.json'
        # print(commond)
        subprocess.call(commond, shell=True)
        sleep(1)


if __name__ == '__main__':
    db_util = util.MySQLUtil(host="node1", user="root", passwd="123456", db="gmall")
    tmp2job(db_util, tmp_file='mysql2hdfs.tpl')
    execute_shell(db_util)


