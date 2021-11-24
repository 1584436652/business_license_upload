import os
from random import choice

from pymongo import MongoClient


def find_file(file_path="d:/测试"):
    if os.path.exists(file_path):
        return file_path


def walk_file():
    file = find_file()
    try:
        for root, dirs, files in os.walk(file):
            # root 表示当前正在访问的文件夹路径
            # dirs 表示该文件夹下的子目录名list
            # files 表示该文件夹下的文件list
            # 遍历文件
            print(f"共{len(files)}张营业执照")
            for f in files:
                yield os.path.join(root, f)

            # # 遍历所有的文件夹
            # for d in dirs:
            #     print(os.path.join(root, d))
    except TypeError as e:
        print("当前目录下没有｛营业执照｝文件")
        raise e


def get_files():
    file = find_file()
    mg_dict = {}
    di = []
    try:
        for root, dirs, files in os.walk(file):
            for f1 in files:
                print(os.path.join(root, f1))
            for f2 in dirs:
                print(os.path.join(root, f2))




            #
            # print(dirs)
            mg = []
            # root 表示当前正在访问的文件夹路径
            # dirs 表示该文件夹下的子目录名list
            # files 表示该文件夹下的文件list
            # print(f"共{len(files)}张营业执照"
            # for d in dirs:
            #     print(d)
            # for f in files:
            #     print(f)
            #     mg.append(os.path.join(root, f))
                # if mg:
                #     mg_dict[d] = mg
            # 遍历所有的文件夹
            # for d in dirs:
            #     print(d)
        # print(mg_dict)

    except TypeError as e:
        print("当前目录下没有｛营业执照｝文件")
        raise e


class MongodbIP:
    """
    代理ip
    """

    def __init__(self):
        # mongodb数据库操作对象
        self.client = MongoClient(host='127.0.0.1', port=27017)
        # 数据插⼊的数据库与集合
        self.coll = self.client["IP"]["IPAddressPool"]
        self.__ip_library = []

    @property
    def ip_library(self):
        for ip in self.coll.find({}, {'_id': 0}):
            self.__ip_library.append(ip)
        return self.__ip_library

    @property
    def ip(self):
        use_ip = choice(self.ip_library)
        print("当前使用ip：{}".format(use_ip))
        return use_ip


if __name__ == '__main__':
    # for picture in walk_file():
    #     print(picture)
    get_files()

