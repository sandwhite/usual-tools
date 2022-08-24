# coding=utf-8
import cv2
import numpy as np
import math


def point_contour_dist(hull, points, text, measure_dist=True, max_dist=100, img=None):
    """寻找与轮廓符合距离的凹点

    :param img: 绘制结果图片
    :param hull: 轮廓hull
    :param point: 凹点集合
    :param text: 文本距离
    :param measure_dist: 计算结果方式
    :return: 距离、最远的质心点
    """
    font = cv2.FONT_HERSHEY_SIMPLEX

    ao_points = []
    for point in points:
        distance = cv2.pointPolygonTest(hull, point, measure_dist)
        # ==================================加判断是否是符合的凹点=============================
        if distance > max_dist:
            ao_points.append(point)
            # cv2.putText(img, text, f_point, font, 1, (0, 255, 0), 3)
            print("pit_point{}的距离:".format(point), distance)

    return ao_points


def link_line(img, point1, point2):
    """

    :param point1:
    :param point2:
    :return:图片
    """

    height, width = img.shape[0], img.shape[1]

    x1, y1 = point1[0], point1[1]
    x2, y2 = point2[0], point2[1]

    slope = math.atan((y2 - y1) / (x2 - x1))
    angle = slope / math.pi * 180
    start_point = (0, int(y2 - x2 * math.tan(slope)))
    end_point = (width, int(y2 + (width - x2) * math.tan(slope)))

    color = (0, 0, 0)
    thickness = 6
    # image = cv.line(img, start_point, end_point, color, thickness)
    image = cv2.line(img, start_point, end_point, color, thickness)
    return image


def step_1(img, save_ostu=False, save_close=False, save_open=False, show_pic=False):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, ostu_pic = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    # ret, ostu_pic = cv2.threshold(img_gray, 250, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    # ret, ostu_pic = cv2.threshold(img_gray, 100, 255, cv2.THRESH_BINARY)
    if save_ostu:
        cv2.imwrite('ostu_pic.jpg', ostu_pic)

    element = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))  # 结构元素
    close_pic = cv2.morphologyEx(ostu_pic, cv2.MORPH_CLOSE, element, iterations=5)  # 先膨胀后腐蚀 # 填充内部孔隙
    if save_close:
        cv2.imwrite('close_pic.jpg', close_pic)

    element_OPEN = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))  # 结构元素
    open_pic = cv2.morphologyEx(close_pic, cv2.MORPH_OPEN, element_OPEN, iterations=5)  # 先腐蚀后膨胀  # 美化外轮廓
    if save_open:
        cv2.imwrite('open_pic.jpg', open_pic)

    if show_pic:
        cv2.imshow('ostu_pic', ostu_pic)
        cv2.imshow('close_pic', close_pic)
        cv2.imshow('open_pic', open_pic)
        cv2.waitKey(0)
    return open_pic


def step_2(thresh, save_pic=False, show_pic=False, draw_pic=False):
    thresh1 = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)

    img_c, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # print('轮廓数目:', len(contours))

    for cnt in contours:
        # 遍历轮廓,检测凹点
        hull_ao = cv2.convexHull(cnt, returnPoints=False)  # returnPoints=False是为了检测凹包使用
        defects = cv2.convexityDefects(cnt, hull_ao)
        collect = []  # 凹点集合
        if defects is None:  # 如果全部都是凸点则跳过
            continue
        for i in range(defects.shape[0]):
            s, e, f, d = defects[i, 0]
            start = tuple(cnt[s][0])
            end = tuple(cnt[e][0])
            far = tuple(cnt[f][0])  # 凹点
            # print(start, end, far, d)
            collect.append(far)
            # cv2.line(img, start, end, [0, 255, 0], 2)
            # cv2.circle(img, far, 5, [0, 0, 255], -1)
        # 质心
        mu = cv2.moments(cnt, False)
        mc = (mu['m10'] / mu['m00'], mu['m01'] / mu['m00'])

        # print('质心：|{:0.1f}, {:0.1f}|'.format(mc[0], mc[1]))

        hull = cv2.convexHull(cnt)  # 检测凸包

        points_ao = point_contour_dist(img=thresh1, hull=hull, points=collect, text="A", max_dist=100)  # 是一个集合

        if draw_pic:
            cv2.circle(thresh1, (int(mc[0]), int(mc[1])), 5, [0, 0, 255], -1)  # 画质心
            cv2.polylines(thresh1, [hull], True, (255, 0, 0), 2)  # 画外轮廓
            for point in points_ao:
                cv2.circle(thresh1, point, 5, [0, 255, 0], -1)  # 画凹点

        if show_pic:
            cv2.imshow('draw_points', thresh1)
            cv2.waitKey(0)
        if save_pic:
            cv2.imwrite('draw_points.jpg', thresh1)



        for point in points_ao:
            thresh1 = link_line(thresh1, mc, point)

        if show_pic:
            cv2.imshow("img_split", thresh1)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        if save_pic:
            cv2.imwrite('split_2.jpg', thresh1)
    return thresh1


if __name__ == '__main__':
    # 进行ostu操作
    img = cv2.imread('./init_pic_1.png')
    thresh = step_1(img, show_pic=True)
    step_2(thresh, show_pic=True, draw_pic=True)
