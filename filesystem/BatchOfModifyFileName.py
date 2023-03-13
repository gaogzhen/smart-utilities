# 批量修改文件名
import os
import time
import re

if __name__ == '__main__':
    root = "L:\BaiduSyncdisk\study\DataStructureAndAlgorithms\java\data-structure\graph/01undirected\images/"
    root = root.replace('\\', '/')

    # 如果文件不以数字开头，添加时间字符串比如20230313
    num_start_rule = re.compile('^\\d+')
    files = os.listdir(root)
    for filename in files:
        if not num_start_rule.match(filename):
            # print(time.strftime('%Y%m%d', time.localtime(int(time.time()))))
            s = time.strftime('%Y%m%d', time.localtime(int(time.time())))
            old_filename = root + filename
            new_filename = root + s + '-' + filename
            # print(new_filename)
            # print(old_filename)
            os.rename(old_filename, new_filename)
