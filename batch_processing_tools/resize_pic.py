import os
from PIL import Image
import sys


# 获取path目录下的所有文件
def get_imlist(path):
    return [os.path.join(path, f)
            for f in os.listdir(path)]


def change_size(path):
    directorys = get_imlist(path)
    for directory in directorys:
        # 不是图片文件就跳过
        print(directory)
        if not (directory.endswith('.jpg') or directory.endswith('.png') or directory.endswith('.bmp')):
            pass
        else:
            img = Image.open(directory)
            s = "/"
            # 获取文件名（含后缀）
            oimage_name = directory[directory.rfind(s) + 1:]
            (oimage_width, oimage_height) = img.size
            new_width = int(32)
            new_height = int(40)
            out = img.resize((new_width, new_height), Image.ANTIALIAS)
            out.save("%s" % oimage_name)  # 直接替换

if __name__ == '__main__':
    change_size(r"E:\plate-recognition\车牌图片\中文字符\zh_zhe")
