# coding=utf-8
import cv2
import numpy as np
import matplotlib.pyplot as plt


# 突出图像中的细节,锐化

def laplacian(image):
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    image_lap = cv2.filter2D(image, cv2.CV_8UC3, kernel)
    return image_lap

def L(img):
    kernel = np.array([[0, -1, 0], [0, 5, 0], [0, -1, 0]])  # 定义卷积核
    imageEnhance = cv2.filter2D(img, -1, kernel)  # 进行卷积运算
    return imageEnhance

if __name__ == "__main__":
    image = cv2.imread("../origin_pic/sample7.jpg")


    # image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # ----------------------------------------
    # b = laplacian(image[:, :, 0])
    # g = laplacian(image[:, :, 1])
    # r = laplacian(image[:, :, 2])
    # image_lap = cv2.merge([b, g, r])
    # ----------------------------------------

    image_lap = laplacian(image)

    cv2.imwrite('lap_low.jpg', image_lap)
    cv2.namedWindow('result', cv2.WINDOW_NORMAL)
    cv2.imshow('result', image_lap)
    cv2.waitKey(0)
    # plt.subplot(1, 1, 1)
    # plt.imshow(image_lap)
    # plt.axis('off')
    # plt.title('laplacian_enhance')
