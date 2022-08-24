# coding=utf-8
import matlab.engine
import time
import cv2
import numpy as np
from detect_pits import step_1, step_2
from show import findPlateNumberRegion, coordinate
import os
from MR.live_demo import step_detct
from enhance_laplacian import laplacian
from CLAHE_Augment import step_CLAHE_process


def manifold_detect(eng):
    t0 = time.time()
    ass = eng.demo()
    t1 = time.time()
    print('图模型推理时间{:0.3f}s'.format(t1 - t0))
    return ass


def batch_detct(dic_path, MR_path, need_preprocess=0, start_matlab=True):
    # 进行松果图像预处理
    # 1.列出文件夹中的所有图片
    file_list = os.listdir(dic_path)

    if need_preprocess == 1:
        for tag, content in enumerate(file_list):
            if content.endswith('bmp'):
                continue
            img_path = dic_path + '/' + content
            src = cv2.imread(img_path)  # 原图

            # 双边滤波
            bilateral = cv2.bilateralFilter(src, d=10, sigmaColor=50, sigmaSpace=50)

            # CLAHE

            # CLAHE_img = step_CLAHE_process(src)

            # 图像增强
            image_lap = laplacian(bilateral)
            # cv2.imwrite(img_path, image_lap)
        print('所有图像预处理完成！！！！！！')

    # 1、法一
    # 对文件夹里的所有图片进行显著性检测
    if start_matlab:
        eng = matlab.engine.start_matlab()
        manifold_detect(eng)
        eng.quit()
    print('所有图像显著性检测完成！！！！！！')

    for tag, content in enumerate(file_list):
        print('-------------------------{}---------------------'.format(tag))
        if content.endswith('bmp'):
            continue

        img_path = dic_path + '/' + content
        src = cv2.imread(img_path)  # 原图

        # ------------------------------------- 显著性图片读取--------------------------------
        manifold_pic = cv2.imread(MR_path + '/' + content[:-4] + '_stage2.jpg')
        # manifold_pic = step_detct(image_lap)

        # cv2.imshow('manifold_pic', manifold_pic)
        # cv2.waitKey(0)

        # ------------------------------------- 显著性图片读取--------------------------------

        thresh = step_1(manifold_pic, show_pic=False)  # 进行图像杂质的滤除
        try:
            mask = step_2(thresh, show_pic=False, draw_pic=False)  # 寻找轮廓
        except Exception as e:
            print('无法在图像{}中找到松果'.format(content[:-4]))
            print('原因:{}'.format(e))
            continue

        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        ret, mask = cv2.threshold(mask, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        # cv2.imshow('mask', mask)
        # cv2.waitKey(0)

        # 标记轮廓
        region = findPlateNumberRegion(mask)
        for i in region:
            cv2.drawContours(src, [i], 0, (255, 0, 0), 8)
            box = coordinate(i)
            # print('轮廓的矩形坐标', box)
        print('-------------------------{}---------------------'.format("分割线"))

        cv2.imwrite('./save_pic/ons_{}.jpg'.format(content[:-4]), src)
        # cv2.namedWindow("img", cv2.WINDOW_GUI_NORMAL)
        # cv2.imshow("img", src)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()


if __name__ == "__main__":
    dic_path = './test'
    MR_path = './saliencymap'
    t0 = time.time()
    batch_detct(dic_path, MR_path)
    t1 = time.time()
    print('平均检测时间：{:0.3f}s'.format((t1-t0)/200))