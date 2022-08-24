import cv2 as cv
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
from matplotlib.font_manager import FontProperties

config = {
    "font.family": 'serif',
    "font.size": 18,
    "mathtext.fontset": 'stix',
    "font.serif": ['SimSun'],
}
mpl.rcParams.update(config)


# plt.title(r'宋体 $\mathrm{Times \; New \; Roman}\/\/ \alpha_i > \beta_i$')
# plt.axis('off')
# plt.savefig("usestix.png")

def localEqualHist(Img):
    # gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    clahe = cv.createCLAHE(clipLimit=5, tileGridSize=(7, 7))  # 原来是7*7
    dst = clahe.apply(Img)
    # cv.namedWindow("clahe image", cv.WINDOW_GUI_NORMAL)
    # cv.imshow("clahe image", dst)
    return dst


def step_CLAHE_process(img):
    b = localEqualHist(img[:, :, 0])  # 效果好
    g = localEqualHist(img[:, :, 1])
    r = localEqualHist(img[:, :, 2])
    image_bgr = cv.merge([b, g, r])
    return image_bgr


def main(path):
    src = cv.imread(path)
    b = localEqualHist(src[:, :, 0])  # 效果好
    g = localEqualHist(src[:, :, 1])
    r = localEqualHist(src[:, :, 2])
    image_bgr = cv.merge([b, g, r])

    cv.imshow('src', src)
    cv.namedWindow('result', cv.WINDOW_GUI_NORMAL)
    cv.imshow('result', image_bgr)
    cv.imwrite('CLAHE.jpg', image_bgr)
    cv.waitKey(0)
    # plt.subplot(121)

    plt.rcParams['xtick.direction'] = 'in'  # 将x周的刻度线方向设置向内
    plt.rcParams['ytick.direction'] = 'in'  # 将y轴的刻度方向设置向内

    x_major_locator = MultipleLocator(50)
    # 把x轴的刻度间隔设置为100，并存在变量里
    y_major_locator = MultipleLocator(50)
    # 把y轴的刻度间隔设置为10，并存在变量里
    ax = plt.gca()
    # ax为两条坐标轴的实例
    ax.xaxis.set_major_locator(x_major_locator)
    # 把x轴的主刻度设置为1的倍数
    ax.yaxis.set_major_locator(y_major_locator)
    # 把y轴的主刻度设置为10的倍数
    # plt.xlim(-0.5, 11)
    # 把x轴的刻度范围设置为-0.5到11，因为0.5不满一个刻度间隔，所以数字不会显示出来，但是能看到一点空白
    plt.ylim(0, 250)
    # 把y轴的刻度范围设置为-5到110，同理，-5不会标出来，但是能看到一点空白

    # 原图的像素直方图
    # plt.xlabel('像素值' + "\n" + "Pixel value")
    # plt.ylabel('像素值个数' + "\n" + "Number of pixel values")
    # plt.hist(src.ravel(), 256)
    # # plt.subplot(122)
    # plt.savefig('src_histogram_equalization.png', bbox_inches='tight')
    # plt.show()

    # CLAHE后的像素直方图
    # plt.xlabel('像素值' + "\n" + "Pixel value")
    # plt.ylabel('像素值个数' + "\n" + "Number of pixel values")
    # plt.hist(image_bgr.ravel(), 256)
    # plt.savefig('processed_histogram_equalization.png',bbox_inches='tight')
    # plt.show()
    return image_bgr


def main2(path):
    src = cv.imread(path)
    b, g, r = cv.split(src)
    b = localEqualHist(b)
    g = localEqualHist(g)
    r = localEqualHist(r)
    image_bgr = cv.merge([b, g, r])

    cv.imshow('src', cv.WINDOW_GUI_NORMAL)
    cv.imshow('src', src)
    cv.namedWindow('result', cv.WINDOW_GUI_NORMAL)
    cv.imshow('result', image_bgr)
    cv.waitKey(0)


def main3(path):
    img = cv.imread(path, cv.IMREAD_COLOR)  # 打开文件
    # 通过cv2.cvtColor把图像从BGR转换到HSV
    img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    changed_hsv = img_hsv.copy()
    changed_hsv[:, :, 2] = 0.6 * changed_hsv[:, :, 2]
    changed_hsv[:, :, 1] = 1.2 * changed_hsv[:, :, 1]
    # changed_hsv[:, :, 0] = (changed_hsv[:, :, 0]+10) % 180  # H 是色调 ， S 是饱和度 ， V是亮度

    darker_img = cv.cvtColor(changed_hsv, cv.COLOR_HSV2BGR)
    cv.namedWindow('result', cv.WINDOW_NORMAL)
    cv.namedWindow('src', cv.WINDOW_NORMAL)
    cv.imshow('result', darker_img)
    cv.imshow('src', img)
    cv.waitKey(0)
    # return H, S, V  # H的范围0-180，S、V的范围是0-255


def main4(path):
    im = cv.imread(path)
    depth = im.shape[2]
    for i in range(im.shape[1]):  # 1是高度
        for j in range(im.shape[0]):
            b = localEqualHist(im[i, j][:, :, 0])  # 这里可以处理每个像素点
            g = localEqualHist(im[i, j][:, :, 1])  # 这里可以处理每个像素点
            r = localEqualHist(im[i, j][:, :, 2])  # 这里可以处理每个像素点
            im[i, j] = cv.merge([b, g, r])
    cv.namedWindow('result', cv.WINDOW_NORMAL)
    cv.imshow('result', im)
    cv.waitKey(0)


num = 0

if __name__ == "__main__":
    # path = "C:/Users/Administrator.OH5LC2FJLY4OLHK/Desktop/common"
    # fileList = os.listdir(path)
    #
    # for file in fileList:
    #    num = num + 1
    #    try:
    #        # location(path + "/" + "origin%d.jpg" % num)
    #        Getimg = main(path + "/" + "origin%d.jpg" % num)
    #        cv.imwrite('C:/Users/Administrator.OH5LC2FJLY4OLHK/Desktop/save/result%d.png' % num, Getimg)
    #    except Exception as E:
    #        print("异常文件:%s;异常原因：%s" % (file, E))

    file = r"../origin_pic/sanmple_one.jpg"
    main(file)

    # try:
    #     main(file)
    # except Exception as E:
    #     print("错误原因:", E)
