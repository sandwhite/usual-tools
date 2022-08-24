# -*- coding: utf-8 -*-
'''
Created on 2013-11-13 09:56
@summary:  Traverse folder and rename
@author: leaf
'''

import os
import os.path

rootdir = r"E:\pp"  # 指明被遍历的文件夹

if __name__ == '__main__':
    i = 0
    for parent, dirnames, filenames in os.walk(rootdir):  # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
        for filename in filenames:  # 文件名
            i = i + 1
            # os.rename(os.path.join(parent, filename), os.path.join(parent, filename[:]+'.bmp'))  # 重命名
            os.rename(os.path.join(parent, filename), os.path.join(parent, 'HS_pinecone_' + str(i) + '.jpg'))  # 重命名
            print(i)
