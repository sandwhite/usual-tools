# coding=utf-8
import os
import sys
import cv2
import shutil
import numpy as np
import matplotlib.pyplot as plt


def getTheBright(path):
    """
    求取图像的亮度值
    :param path: 输入图像路径
    :return: 返回该图像亮度值
    """
    img = cv2.imread(path)
    b, g, r = cv2.split(img)

    avg_b = 0
    avg_g = 0
    avg_r = 0

    sum_b = 0
    sum_g = 0
    sum_r = 0

    for i in range(0, b.shape[0]):
        for j in range(0, b.shape[1]):
            sum_b += b[i][j]
            sum_g += g[i][j]
            sum_r += r[i][j]

    avg_b = int(sum_b / b.shape[0] / b.shape[1])
    avg_g = int(sum_g / g.shape[0] / g.shape[1])
    avg_r = int(sum_r / r.shape[0] / r.shape[1])

    y = int(0.299 * avg_r + 0.587 * avg_g + 0.114 * avg_b)
    return y


def getTheYvalue(original_path):
    """
    获得文件夹下所有图像的Y值
    :return:
    """
    # original_path = "./data/"
    files = os.listdir(original_path)
    # all_Y = []
    fp = open("./illumination-level.txt", "w")
    Len_files = len(files)
    for i in range(0, Len_files):
        if files[i].endswith('.jpg'):
            y = getTheBright(original_path + files[i])
            # all_Y.append(y)
            context = str(files[i]) + ' ' + str(y)
            print('写入文本进度|{:0.2f}%'.format((i + 1) / Len_files * 100))
            fp.write(context + "\n")
    fp.close()


def readTextGetYvalue():
    """
    得到txt文件中的所有Y值
    :return:
    """
    fp = open("./illumination-level.txt", "r+")
    Y = fp.readlines()
    y_value = []
    img_files = []
    for line in Y:
        line = line.rstrip("\n")
        front, back = line.split(' ')
        y_value.append(int(back))
        img_files.append(str(front))
    # print(y_value)
    max_y = max(y_value)
    min_y = min(y_value)
    print('max_brightness:', max_y)
    print('min_brightness:', min_y)

    A, B, C = 0, 0, 0
    for i in range(len(y_value)):
        # score = int((y_value[i] - min_y) / (max_y - min_y) * 10)  # 0-10之间
        # if score < 3:
        #     y_value[i] = 'dim'
        #     A+=1
        # elif score > 4:
        #     y_value[i] = 'bright'
        #     C+=1
        # else:
        #     y_value[i] = 'normal'
        #     B+=1

        if y_value[i] < 90:
            A += 1
        elif y_value[i] < 110:
            B += 1
        else:
            C += 1
    # print(y_value)
    # 区分不开

    x = np.arange(3)
    yl = np.array([A, B, C])
    # 柱形的宽度
    bar_width = 0.3
    # 绘制柱形图
    plt.bar(x, yl, tick_label=['a', 'b', 'c'], width=bar_width)
    plt.show()
    return img_files, y_value


def moveTheOriImageToRightIllumination(ori_path, dst_path):
    """
    根据illumination-level.txt中的结果将illumination_test_images中的图像分配到0-10种亮度等级中
    :return:
    """
    img_files, y_value = readTextGetYvalue()
    # ori_path = "./data/"
    # dst_path = "./results/"

    # img_files = os.listdir(ori_path)  # 文件名

    # L = len(y_value)
    # for i in range(0, L):
    #     print('分类图片进度|{:0.2f}%'.format((i+1)/L*100))
    #     dst_path2 = dst_path + '/' + str(y_value[i]) + '/'
    #     if not os.path.exists(dst_path2):
    #         os.makedirs(dst_path2)
    #     shutil.copy(ori_path + img_files[i], dst_path2 + img_files[i])
    #     try:
    #         shutil.copy(os.path.join(ori_path , img_files[i][:-4]+'.xml'),
    #                     os.path.join(dst_path2 , img_files[i][:-4]+'.xml'))
    #     except:
    #         print('不存在{}.xml文件'.format(img_files[i][:-4]))


if __name__ == '__main__':
    ori_path = "./data/"
    dst_path = "./results/"
    # getTheYvalue(ori_path)  # 获取图像亮度，写入illumination-level.txt
    moveTheOriImageToRightIllumination(ori_path, dst_path)  # 移动图像
