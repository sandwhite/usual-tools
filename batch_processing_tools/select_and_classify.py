# coding=utf-8
import os
import cv2
import shutil


def show_pic(dic_path):
    file_list = os.listdir(dic_path)
    dic_split = dic_path.split('/')
    all_len = len(file_list)
    for tag, content in enumerate(file_list):
        print('分类图片进度|{:0.2f}%'.format((tag + 1) / all_len * 100))
        if content.endswith('.jpg'):
            img_path = os.path.join(dic_path, content)
            img = cv2.imread(img_path)
            cv2.namedWindow('{}'.format(content[:-4]), cv2.WINDOW_AUTOSIZE)
            cv2.moveWindow('{}'.format(content[:-4]), 1, 1)
            cv2.imshow('{}'.format(content[:-4]), img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

            classed_dic = input('文件夹代号：')
            while classed_dic not in ['0', '1', '2']:
                classed_dic = input('文件夹代号：')
            classed_dic = int(classed_dic)
            label_list = ['dim', 'normal', 'bright']
            if label_list[classed_dic] == dic_split[-1]:
                continue
            try:
                shutil.move(img_path, os.path.join('/'.join(dic_split[:-1]) + '/' + label_list[classed_dic], content))
                shutil.move(os.path.join(dic_path, content[:-4] + '.xml'),
                            os.path.join('/'.join(dic_split[:-1]) + '/' + label_list[classed_dic],
                                         content[:-4] + '.xml'))
                print('完成移动第{}个文件'.format(tag))
            except Exception as e:
                print('------------无法移动|{}|文件-----------'.format(content[:-4]))
                print('原因：{}'.format(e))


if __name__ == "__main__":
    dic_path = './results/normal'
    show_pic(dic_path)
