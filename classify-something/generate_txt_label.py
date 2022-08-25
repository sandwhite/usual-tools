# coding:utf-8
import os
import shutil


def IsSubString(SubStrList, Str):
    flag = True

    for substr in SubStrList:
        if not (substr in Str):
            flag = False
    return flag


# 扫面文件
def GetFileList(FindPath, FlagStr=[]):
    FileList = []

    FileNames = os.listdir(FindPath)
    if len(FileNames) > 0:
        for fn in FileNames:
            if len(FlagStr) > 0:
                if IsSubString(FlagStr, fn):
                    fullfilename = os.path.join(FindPath, fn)
                    FileList.append(fullfilename)
            else:
                fullfilename = os.path.join(FindPath, fn)
                FileList.append(fullfilename)

    if len(FileList) > 0:
        FileList.sort()

    return FileList


def get_label(data_path):
    label = os.listdir(data_path)
    label_txt = open('correspond_label.txt', 'w')
    for tag, content in enumerate(label):
        input_data = str(content) + ' ' + str(tag) + '\n'
        label_txt.write(input_data)
    label_txt.close()
    return label


def make_label_txt(train_data_path, label_list, train_img_path, test_img_path):
    label_train_txt = open('train.txt', 'w')
    label_test_txt = open('test.txt', 'w')

    for tag, content in enumerate(label_list):
        label_dic = os.path.join(train_data_path, content)
        trainfile = os.listdir(label_dic)
        all_len = len(trainfile)
        train_len = int(0.8 * all_len)
        for i in range(train_len):
            str2 = trainfile[i] + ' ' + str(tag) + '\n'  # 生成训练文本标签
            label_train_txt.write(str2)
            A = os.path.join(train_img_path, trainfile[i])
            shutil.copy(os.path.join(label_dic, trainfile[i]), os.path.join(train_img_path, trainfile[i]))

        for j in range(train_len, all_len):
            tests_label = trainfile[j] + ' ' + str(tag) + '\n'  # 生成测试文本标签
            label_test_txt.write(tests_label)
            shutil.copy(os.path.join(label_dic, trainfile[j]), os.path.join(test_img_path, trainfile[j]))

    # 转换完成后，将.txt文档关闭
    label_train_txt.close()
    label_test_txt.close()

    print("成功生成训练和测试文件！")


if __name__ == "__main__":
    train_data_path = './train_data/'
    train_img_path, test_img_path = './train_images', './test_images'
    label = get_label(train_data_path)
    make_label_txt(train_data_path, label, train_img_path, test_img_path)
