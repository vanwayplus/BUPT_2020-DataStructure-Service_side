# -*- encoding:utf-8 -*-
from hashlib import md5
import os


def generate_file_md5value(fpath):
    '''以文件路径作为参数，返回对文件md5后的值
    '''
    m = md5()
    # 需要使用二进制格式读取文件内容
    a_file = open(fpath, 'rb')
    m.update(a_file.read())
    a_file.close()
    return m.hexdigest()


def generate_file_md5sumFile(fpath):
    fname = os.path.basename(fpath)
    fpath_md5 = "%s.md5" % fpath
    fout = open(fpath_md5, "w")
    fout.write("%s %s\n" % (generate_file_md5value(fpath), fname.strip()))
    print
    "generate success, fpath:%s" % fpath_md5
    fout.flush()
    fout.close()


if __name__ == "__main__":
    fpath = "C:\\Users\\littl\\PycharmProjects\\fastApiProject2\\temp\\input2c.txt"
    # 测试一：以文件路径作为参数，获得md5后的字符串
    print(generate_file_md5value(fpath))

    # 测试二：生成和linux命令：md5sum同样结果的.md5文件
  #  generate_file_md5sumFile(fpath)