import glob
import os
import shutil
origin_path = 'C:/Users/Administrator/Desktop/label/rgb_pic/'
save_path = 'C:/Users/Administrator/Desktop/label/rgb_valid'

filenames = os.listdir(origin_path)
num = 0
for filename in filenames:
    # if(filename.endswith('.jpg')):
    num = num + 1
    if((num%5)==0):
        shutil.move(os.path.join(origin_path, filename), save_path)
        print(filename)  # 仅仅是为了测试


