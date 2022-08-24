import glob
import cv2
import os
path = 'J:\img1'
save_path = 'C:/Users/Administrator.OH5LC2FJLY4OLHK/Desktop/111'

# path = 'C:/Users/Administrator.OH5LC2FJLY4OLHK/Desktop/origin'
# save_path = 'C:/Users/Administrator.OH5LC2FJLY4OLHK/Desktop/222'

path_file_number=glob.glob(path)#或者指定文件下个数
# path_file_number=glob.glob(pathname='*.py') #获取当前文件夹下个数
# print(path_file_number)
# print(len(path_file_number))

# 读取函数，用来读取文件夹中的所有函数，输入参数是文件名
filenames = os.listdir(path)


filenames.sort()
def read_directory(directory_name):
    num = 0
    for filename in filenames[500:]:
        num = num + 1
        print(filename)  # 仅仅是为了测试
        img = cv2.imread(directory_name + "/" + filename)
        cv2.imwrite(save_path + "/" + filename, img)
        if num == 500:
            break

if __name__ == '__main__':
    read_directory(path)  #这里传入所要读取文件夹的绝对路径，加引号（引号不能省略！）

