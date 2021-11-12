import os


def find_file(file_path="d:/营业执照"):
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


if __name__ == '__main__':
    for picture in walk_file():
        print(picture)
