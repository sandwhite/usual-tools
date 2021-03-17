# -*- coding: utf-8 -*-
'''
Created on 2021-2-11
@summary:  Traverse folder and rename
@author: DJ
'''

import os
import os.path

rootdir = r"C:\Users\Administrator.OH5LC2FJLY4OLHK\Desktop\origin"  # 指明被遍历的文件夹

i = 0
for parent, dirnames, filenames in os.walk(rootdir):  # 三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
    for filename in filenames:  # 文件名
        i = i + 1
        # os.rename(os.path.join(parent, filename), os.path.join(parent, filename[:]+'.bmp'))  # 重命名
        os.rename(os.path.join(parent, filename), os.path.join(parent, 'origin' + str(i) + '.jpg'))  # 重命名
        # print(i)
        
        
        assemble.append(filename+'对应'+str(s))

str1 = '\n'
f=open("parameter_depth.txt",'w')
f.write(str1.join(assemble))
f.close()
print(assemble)
