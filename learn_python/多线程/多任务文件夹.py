import os
import multiprocessing


def copy_file(file_name, old_folder_name, new_folder_name):
    """完成文件的复制"""
    old_f = open(old_folder_name + "/" + file_name, "rb")
    content = old_f.read()
    old_f.close()

    new_f = open(new_folder_name + "/" + file_name, "wb")
    new_f.write(content)
    new_f.close()

    # 如果拷贝完了文件 那么就向队列中写入一个消息，表示已完成



def main():
    # 1.获取用户要copy的文件夹名字

    old_folder_name = input("请输入要copy的文件夹的名字：")
    # 2.创建一个新的文件夹
    try:
        new_folder_name = old_folder_name + "[复件]"
        os.makedirs(new_folder_name)
    except:
        pass

    # 3.获取文件夹的所有要copy的文件名字
    file_names = os.listdir(old_folder_name)
    # print(file_names)
    # 4.创建进程池
    po = multiprocessing.Pool(5)

    # 5.创建一个队列
    q = multiprocessing.Manager().Queue()

    # 5.向进程池中添加拷贝文件的任务
    for file_name in file_names:
        po.apply_async(copy_file, args=(file_name, old_folder_name, new_folder_name))
        q.put(file_name)
    po.close()
    # po.join()
    all_file_num = len(file_names)  # 测试一些所有文件的个数
    copy_num = 0
    while True:
        file_name = q.get()
        print("已经完成copy：%s" % file_name)
        copy_num += 1
        print("\r拷贝进度为：%.2f %%" % (copy_num*100 / all_file_num), end="")
        if copy_num >= all_file_num:
            break
    # print()


if __name__ == "__main__":
    main()
