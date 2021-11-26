import os
import re
from PIL import Image


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
    except TypeError as e:
        print("当前目录下没有｛营业执照｝文件")
        raise e


def get_files():
    file1 = find_file()
    gm = []
    try:
        for root, dirs, files in os.walk(file1):
            # root 表示当前正在访问的文件夹路径
            # dirs 表示该文件夹下的子目录名list
            # files 表示该文件夹下的文件list
            for f in files:
                gm.append(os.path.join(root, f))
        return gm
    except TypeError as e:
        print("当前目录下没有｛营业执照｝文件")
        raise e


def set_files():
    gm_name = {}
    f = get_files()
    for fa in f:
        file_name = get_file_name(fa)
        if file_name not in gm_name:
            gm_name[file_name] = [fa]
        else:
            gm_name[file_name].append(fa)
    return gm_name


def get_file_name(names):
    """
    提取文件夹名
    :param names:
    :return:
    """
    co = re.findall(r'[\\](.+?)[\\]', names, re.S)[0]
    co = re.sub("[A-Za-z0-9\!\%\[\]\,\。]", "", co)
    return co


def file_size(size):
    if os.path.getsize(size) > 7000000:
        print(f"{size}文件大小超出规定大小,正在处理图片")
        resize_image(size, size)


def resize_image(pass_in, efferent, scale=0.6):
    """
    :param pass_in: 输入图片
    :param efferent: 输出图片
    :param scale:
    :return:
    """
    img = Image.open(pass_in)
    width = int(img.size[0] * scale)
    height = int(img.size[1] * scale)
    img_type = img.format
    out = img.resize((width, height), Image.ANTIALIAS)
    # 第二个参数：
    # Image.NEAREST ：低质量
    # Image.BILINEAR：双线性
    # Image.BICUBIC ：三次样条插值
    # Image.ANTIALIAS：高质量
    out.save(efferent, img_type)


if __name__ == '__main__':
    print(file_size('柳林县荞歌红电子商务有限公司.png'))
    print(type(file_size('柳林县荞歌红电子商务有限公司.png')))
