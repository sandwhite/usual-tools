# coding=utf-8
from PIL import Image
import numpy as np
import tensorflow as tf
import os
import shutil
import matplotlib.pyplot as plt
from tensorflow.keras.layers import Conv2D, BatchNormalization, Activation, MaxPool2D, Dropout, Flatten, Dense, \
    MaxPooling2D

model_save_path = './checkpoint/my_model.ckpt'

model = tf.keras.models.Sequential([
    Conv2D(8, (5, 5), activation='relu', input_shape=(150, 150, 1)),
    MaxPooling2D(2, 2),

    Conv2D(16, (5, 5), activation='relu'),
    BatchNormalization(),
    MaxPooling2D(2, 2),

    Conv2D(32, (5, 5), activation='relu'),
    MaxPooling2D(2, 2),

    Flatten(),
    Dense(64, activation='relu'),
    Dense(3, activation='sigmoid')
])

model.load_weights(model_save_path)


def predict(img_path):
    img = Image.open(img_path)
    img = img.resize((150, 150), Image.ANTIALIAS)
    img_arr = np.array(img.convert('L'))
    img_arr = img_arr / 255.0
    x_predict = img_arr[tf.newaxis, ..., tf.newaxis]
    result = model.predict(x_predict)

    pred = tf.argmax(result, axis=1)

    if pred[0] == 0:
        endresult = "bright"
    elif pred[0] == 1:
        endresult = "dim"
    elif pred[0] == 2:
        endresult = "normal"

    # print('\n')
    # print("预测的结果是：%s|%d" % (endresult,pred[0]))
    label_list = ["bright", "dim", "normal"]
    return label_list[pred[0]]


def class_by_predict(img_path, move_path):
    count = 12306
    img_file_list = os.listdir(img_path)
    for filename in img_file_list:
        count -= 1
        print(count)
        if filename.endswith('.jpg'):
            img_file = img_path+'/'+ filename

            label_str = predict(img_file)
            try:
                shutil.copy(img_file, os.path.join(move_path + '/' + label_str, filename))
                shutil.copy(os.path.join(img_path, filename[:-4] + '.xml'),
                            os.path.join(move_path + '/' + label_str, filename[:-4] + '.xml'))
            except:
                print('------------无法移动|{}|文件-----------'.format(filename[:-4]))


if __name__ == '__main__':
    img_path = './data'
    move_path = './results'
    class_by_predict(img_path, move_path)
