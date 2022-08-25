# coding = utf-8
from PIL import Image, ImageStat
import math
import os
import matplotlib.pyplot as plt
import numpy as np
import cv2
import shutil


# 将所有的图片根据亮度值分成4个区间，能看出不同的亮度值对模型的影响。比如有的论文按80，130将图片分为Low，Middle和High。

def brightness(im_file):
    im = Image.open(im_file)
    stat = ImageStat.Stat(im)
    r, g, b = stat.mean
    return math.sqrt(0.241 * (r ** 2) + 0.691 * (g ** 2) + 0.068 * (b ** 2))


# def illumination_averge(directory_name):
#     illumination_averge = []
#     for filename in os.listdir(directory_name):
#         # 用os库读取文件夹内所有图片名称以操作
#         # print(filename)
#         # img = Image.open(directory_name + "/" + filename)
#         im_file = directory_name + "/" + filename
#         illumination_averge.append(brightness(im_file))
#     return illumination_averge

def makesDir(filepath):  # 判断如果文件不存在,则创建
    if not os.path.exists(filepath):
        os.makedirs(filepath)


def illumination_averge(directory_name):
    real_query_dim = './real_query_dim'
    real_query_normal = './real_query_normal'
    real_query_bright = './real_query_bright'

    makesDir(real_query_dim)
    makesDir(real_query_normal)
    makesDir(real_query_bright)

    count = 0
    min_brightness = 1000
    max_brightness = 0

    for filename in os.listdir(directory_name):
        # 用os库读取文件夹内所有图片名称以操作
        # print(filename)
        # img = Image.open(directory_name + "/" + filename)
        if filename.endswith('.jpg'):
            im_file = directory_name + "/" + filename
            count += 1
            im_file_b = brightness(im_file)
            min_brightness = min(im_file_b, min_brightness)
            max_brightness = max(im_file_b, max_brightness)
            print('{}:{}|brightness={}|'.format(count, filename, im_file_b))

            # filename = filename[:-4]
            # f_jpg = filename + '.jpg'
            # f_xml = filename + '.xml'
            # if im_file_b < 80:
            #     try:
            #         shutil.copy(os.path.join(directory_name, f_jpg), os.path.join(real_query_dim, f_jpg))
            #         shutil.copy(os.path.join(directory_name, f_xml), os.path.join(real_query_dim, f_xml))
            #     except:
            #         pass
            # elif im_file_b >= 80 and im_file_b <= 100:
            #     try:
            #         shutil.copy(os.path.join(directory_name, f_jpg), os.path.join(real_query_normal, f_jpg))
            #         shutil.copy(os.path.join(directory_name, f_xml), os.path.join(real_query_normal, f_xml))
            #     except:
            #         pass
            # else:
            #     try:
            #         shutil.copy(os.path.join(directory_name, f_jpg), os.path.join(real_query_bright, f_jpg))
            #         shutil.copy(os.path.join(directory_name, f_xml), os.path.join(real_query_bright, f_xml))
            #     except:
            #         pass
    print('|min_brightness:{:0.3f}|max_brightness:{:0.3f}|'.format(min_brightness,max_brightness))

def draw_hist(directory_name):
    illumination_averges = illumination_averge(directory_name)
    # plt.figure(figsize=(15,5))
    # nums,bins,patches = plt.hist(illumination_averges,bins=20,edgecolor='k') #bins:区间个数 ,nums:这个参数是指定每个bin(箱子)分布的数据,对应x轴,pathes
    # plt.xlabel("Illumination")
    # plt.ylabel("Image Numbers")
    # from IPython import embed
    # embed()
    # from IPython import embed
    # embed()
    # for num,bin in zip(nums,bins):
    #     plt.annotate(num,xy=(bin,num),xytext=(bin,num))
    # plt.show()


if __name__ == '__main__':
    directory_name = 'real_query_normal'
    draw_hist(directory_name)
