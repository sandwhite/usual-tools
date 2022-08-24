# coding=utf-8
import cv2
import numpy as np
from detect_pits import step_1, step_2

# from detect.base_graph_SLIC_manifold_detect import manifold_detect

minPlateRatio = 0.2  # 最小比例
maxPlateRatio = 6  # 最大比例
import time


def findPlateNumberRegion(img):
    # 查找符合面积的轮廓
    region = []
    # 查找外框轮廓
    contours_img, contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  # 适用于opencv3

    # print("contours lenth is :%s" % (len(contours)))
    # 筛选面积小的
    list_rate = []
    for i in range(len(contours)):
        cnt = contours[i]
        # 计算轮廓面积
        area = cv2.contourArea(cnt)
        # 面积小的忽略
        if area < 5000:
            continue
        # 转换成对应的矩形（最小）
        rect = cv2.minAreaRect(cnt)
        # cv2.minEnclosingCircle()
        # circle = cv2.minEnclosingCircle(cnt)

        # print("rect is:%s" % {rect})
        # 根据矩形转成box类型，并int化
        box = np.int32(cv2.boxPoints(rect))
        # 计算高和宽
        height = abs(box[0][1] - box[2][1])
        width = abs(box[0][0] - box[2][0])
        # 正常情况车牌长高比在2.7-5之间,那种两行的有可能小于2.5，这里不考虑
        ratio = float(width) / float(height)
        rate = getxyRate(cnt)
        # print("area", area, "ratio:", ratio, "rate:", rate)
        # if ratio > maxPlateRatio or ratio < minPlateRatio:
        #     continue
        # 符合条件，加入到轮廓集合
        region.append(box)
        list_rate.append(ratio)
    # index = getSatifyestBox(list_rate)
    # return region[index]
    return region


# 找出最有可能是车牌的位置
def getSatifyestBox(list_rate):
    for index, key in enumerate(list_rate):
        list_rate[index] = abs(key - 3)
    # print(list_rate)
    index = list_rate.index(min(list_rate))
    # print(index)
    return index


def getxyRate(cnt):
    x_height = 0
    y_height = 0
    x_list = []
    y_list = []
    for location_value in cnt:
        location = location_value[0]
        x_list.append(location[0])
        y_list.append(location[1])
    x_height = max(x_list) - min(x_list)
    y_height = max(y_list) - min(y_list)
    return x_height * (1.0) / y_height * (1.0)


def coordinate(box):
    # 求box各坐标点 ,box是轮廓的矩形点
    # 返回区域对应的图像
    # 因为不知道，点的顺序，所以对左边点坐标排序

    ys = [box[0, 1], box[1, 1], box[2, 1], box[3, 1]]
    xs = [box[0, 0], box[1, 0], box[2, 0], box[3, 0]]
    ys_sorted_index = np.argsort(ys)
    xs_sorted_index = np.argsort(xs)

    # 获取x上的坐标
    x1 = box[xs_sorted_index[0], 0]
    x2 = box[xs_sorted_index[3], 0]

    # 获取y上的坐标
    y1 = box[ys_sorted_index[0], 1]
    y2 = box[ys_sorted_index[3], 1]

    # 截取图像
    # print('box:', (x1, y1), (x2, y2))
    # img_plate = img[y1:y2, x1:x2]
    return (x1, y1), (x2, y2)


if __name__ == "__main__":

    manifold_detect()

    t0 = time.time()
    src = cv2.imread('../origin_pic/sample5.jpg')  # 原图

    # 得到掩模图版
    manifold_pic = cv2.imread('../show/sample_stage2.png')

    thresh = step_1(manifold_pic, show_pic=False)
    mask = step_2(thresh, show_pic=False, draw_pic=False)
    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(mask, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    # cv2.imshow('mask', mask)
    # cv2.waitKey(0)

    # 标记轮廓
    region = findPlateNumberRegion(mask)
    for i in region:
        cv2.drawContours(src, [i], 0, (255, 0, 0), 8)
        box = coordinate(i)
        print('轮廓的矩形坐标', box)
    t1 = time.time()
    print('整体消耗时间：', t1 - t0)

    # cv2.imwrite('detect1.jpg', src)
    cv2.namedWindow("img", cv2.WINDOW_GUI_NORMAL)
    cv2.imshow("img", src)
    cv2.waitKey(0)
