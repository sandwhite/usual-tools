# coding=utf-8
import cv2
import numpy as np


def sort_by_HSV(img_path):
    front,back = img_path.split('/')
    img = cv2.imread(img_path)
    # 将图片转换为HSV格式， 并指定亮度
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # res[:,:,1]=1 # 饱和度
    # res[:, :, 0] = 150  # 色调

    data_v = img_hsv[:, :, 2]
    row_sum = 0
    H, W = data_v.shape
    for i in range(len(data_v)):
        # print(max(data_v[i]))
        row_sum += sum(data_v[i]) / W
        # print(i)
    # print(data_v[0])
    mean_v = row_sum / H
    print('dj--{}|{:0.3f}'.format(back[:-4],mean_v))
    # print(data_v)


    H, S, V = cv2.split(img_hsv)
    # print(V)

    # 亮度（V）
    v = V.ravel()[np.flatnonzero(V)]  # 亮度非零的值
    average_v = sum(v) / len(v)  # 计算亮度均值
    print('network--{}|{:0.3f}'.format(back[:-4],average_v))



if __name__ == "__main__":
    img_path = 'data/M_N_S_1008.jpg'
    sort_by_HSV(img_path)
