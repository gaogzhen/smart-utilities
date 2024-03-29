# 通过datax把mysql中数据全量同步到hdfs，一个表对应一个同步文件。通过模版文件生成job
import pathlib
import subprocess
from string import Template
from time import sleep

import MySQLUtil


# 读取mysql数据，生成datax gmall
def tmp2job(db_util, tmp_file):
    # 获取模版文件
    tmp_file = pathlib.Path(__file__).parent.joinpath(tmp_file)
    # 生成文件路径
    target_dir = pathlib.Path(__file__).parent.joinpath('gmall')
    # 获取全部表名
    db_util.select_db("gmall")
    tables = db_util.list_tables()
    for table in tables:
        if table == 'z_log':
            continue
        target_file = target_dir.joinpath(table + '.json')
        with open(tmp_file, mode="r", encoding="utf-8") as r_f, open(
                target_file, mode="w", encoding="utf8"
        ) as w_f:
            template_content = r_f.read()
            print(f"template_content:{template_content}")
            template = Template(template_content)
            data = template.substitute(table_name=table)
            w_f.write(data)
# 执行job脚本
def execute_shell():
    cmd_ls = 'ls /export/server/datax/job/gmall'
    name = subprocess.check_output(cmd_ls, shell=True)
    names = str(name, encoding='utf-8').split('\n')[:-1]
    for name in names:
        commond = "python3 /export/server/datax/bin/datax.py  /export/server/datax/job/mall/" + name
        subprocess.call(commond, shell=True)
        sleep(1)

if __name__ == '__main__':
    db_util = MySQLUtil(host="127.0.0.1", user="root", passwd="123456", db="gmall")
    tmp2job(db_util, tmp_file='mysql2hdfs.tpl')
    execute_shell()