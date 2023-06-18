#python批量读取excel csv文件插入mysql数据库

import csv
import os

import pymysql


class ConnectionDatabase(object):
    # 连接mysql数据库
    def __init__(self, ip, username, passwd, db, char='utf8'):
        self.ip = ip
        # self.port = port
        self.username = username
        self.passwd = passwd
        self.mysqldb = db
        self.char = char

        self.MySQL_db = pymysql.connect(
            host=self.ip,
            user=self.username,
            password=self.passwd,
            database=self.mysqldb,
            charset=self.char)

    def mysql_findList(self, sql):
        cursor = self.MySQL_db.cursor()
        MySQL_sql = sql
        results = None
        if not cursor:
            raise (NameError, "数据库连接失败")
        try:
            # 执行SQL语句
            cursor.execute(MySQL_sql)
            # 获取所有记录列表
            results = cursor.fetchall()
        except Exception as e:
            print(e)
            self.MySQL_db.close()
        if results:
            return results
        else:
            return None

    # 数据增删改查（sqlserver）
    def mysql_exe_sql(self, sql, params):
        cursor = self.MySQL_db.cursor()
        MySQL_sql = sql
        result = 0
        if not cursor:
            raise (NameError, "数据库连接失败")
        try:
            # 执行SQL语句
            self.MySQL_db.ping(True)
            cursor.execute(MySQL_sql, params)
            result = cursor.rowcount
        except Exception as e:
            print(e)
            self.MySQL_db.rollback()
            self.MySQL_db.close()

        return result > 0

    '''
        提交数据
    '''
    def commitData(self):
        try:
            self.MySQL_db.commit()
        except Exception as e:
            print(e)

    '''
        关闭数据库连接
    '''
    def closeConn(self):
        if self.MySQL_db:
            self.MySQL_db.close()


'''
    读取文件夹下的csv文件
'''
def readAllFiles(filePath):
    fileList = os.listdir(filePath)
    i = 0
    for file in fileList:
        if file.endswith('.csv'):
            path = os.path.join(filePath, file)
            if os.path.isfile(path):
                file = open(path, 'r', encoding='utf-8')
                print(path)
                i += 1
                print("插入第>>>>", i, ">>>>数据表")
                analysisWorkflowCsv(file)
                pass
            else:
                readAllFiles(path)


def analysisWorkflowCsv(file):
    csvFile = csv.reader(file)
    # 读取一行，下面的reader中已经没有该行了
    # head_row = next(csvFile)
    # print(head_row)
    __conn = ConnectionDatabase(ip="localhost", username="root", passwd="root1234", db="gaogzhen", char="utf8")
    counter = 0
    for row in csvFile:
        print(row)
        data = {}
        # 获取excel内需要的数据,从0开始,根据导入的csv文件的列数来决定data的容量
        data['id'] = row[0]
        data['sn'] = '' + row[1]
        data['name'] = '' + row[2]
        data['price'] = row[3]
        data['num'] = row[4]
        data['alert_num'] = row[5]
        data['image'] = '' + row[6]
        data['images'] = '' + row[7]
        data['weight'] = row[8]
        data['create_time'] = '' + row[9]
        data['update_time'] = '' + row[10]
        data['category_name'] = '' + row[11]
        data['brand_name'] = '' + row[12]
        data['spec'] = '' + row[13]
        data['sale_num'] = row[14]
        data['comment_num'] = row[15]
        data['status'] = row[16]
        print(data)
        if insert_data(__conn, data):
            counter += 1
        if counter % 1000 == 0:
            __conn.commitData()
    print("已经插入工作流数据： %d 条。" % counter)
    __conn.commitData()
    __conn.closeConn()


'''
    插入工作流程数据
'''
def insert_data(__conn, data):
    # 在mysql建立表，字段名可以根据需要设置，也可以按a,b,c这样的简单记录也可以。跟data容量的一一对应。
    __sql = '''
        INSERT INTO `gaogzhen`.`tb_sku` (
      `id`,
      `sn`,
      `name`,
      `price`,
      `num`,
      `alert_num`,
      `image`,
      `images`,
      `weight`,
      `create_time`,
      `update_time`,
      `category_name`,
      `brand_name`,
      `spec`,
      `sale_num`,
      `comment_num`,
      `status`
    )
    VALUES
      (
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s
      )
    '''

    __params = tuple(data.values())
    # print(data)
    # print(__params)
    print(__sql % __params)
    return __conn.mysql_exe_sql(__sql, __params)


if __name__ == "__main__":
    # 文件所在的文件夹父路径,按文件夹下面的文件批量导入
    testFilePath = "/Users/gaogzhen/baiduSyncdisk/study/database"
    readAllFiles(testFilePath)