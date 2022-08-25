# coding=utf-8
import os
from PIL import Image
import sys


# 获取path目录下的所有文件
def get_imlist(path):
    return [os.path.join(path, f)
            for f in os.listdir(path)]


def read_and_write(read_dir, save_dir):
    directorys = get_imlist(read_dir)

    count = 0
    for filename in directorys:
        # 不是图片文件就跳过
        if not (filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.bmp')):
            pass
        else:
            count += 1
            img = Image.open(filename)

            new_width = int(700)
            new_height = int(700)

            out = img.resize((new_width, new_height), Image.ANTIALIAS)  # 第一个参数是用于指定图像的宽高(元组)，
            # 第二个参数指定过滤器类型：NEAREST、BILINER、BICUBIC、ANTALIAS，其中ANTALIAS为最高品质
            out.save(save_dir + 'HS_pinecone_' + str(count) + filename[-4:])  # 直接替换
            print(count)


if __name__ == '__main__':
    read_dir = r"F:\sample_huaguduo"
    save_dir = r'E:/data_pinecone/'

    read_and_write(read_dir=read_dir, save_dir=save_dir)
