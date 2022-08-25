import os
import tensorflow as tf
from PIL import Image
import numpy as np
from tensorflow.keras.layers import Conv2D, BatchNormalization, Activation, MaxPool2D, Dropout, Flatten, Dense, \
    MaxPooling2D
from tensorflow.keras import Model
from matplotlib import pyplot as plt
# 训练集
from tensorflow_core.python.keras.optimizers import RMSprop

train_path = './train_images/'
train_txt = './train.txt'

x_train_savepath = './x_train.npy'
y_train_savepath = './y_train.npy'
# 测试集
test_path = './test_images/'
test_txt = './test.txt'

x_test_savepath = './x_test.npy'
y_test_savepath = './y_test.npy'


# 读取并制作数据集
def generateds(path, txt):
    f = open(txt, 'r')  # 以只读形式打开txt文件
    contents = f.readlines()  # 读取文件中所有行
    f.close()  # 关闭txt文件
    x, y_ = [], []  # 建立空列表
    for content in contents:  # 逐行取出
        value = content.split()  # 以空格分开，图片路径为value[0] , 标签为value[1] , 存入列表
        img_path = path + value[0]  # 拼出图片路径和文件名
        img = Image.open(img_path)  # 读入图片
        img = img.resize((150, 150), Image.ANTIALIAS)  # 尺寸大小为150*150
        img = np.array(img.convert('L'))  # 图片变为8位宽灰度值的np.array格式
        img = img / 255.  # 数据归一化 （实现预处理）
        x.append(img)  # 归一化后的数据，贴到列表x
        y_.append(value[1])  # 标签贴到列表y_
        print('loading : ' + content)  # 打印状态提示

    x = np.array(x)  # 变为np.array格式
    y_ = np.array(y_)  # 变为np.array格式
    y_ = y_.astype(np.int64)  # 变为64位整型
    return x, y_  # 返回输入特征x，返回标签y_


if os.path.exists(x_train_savepath) and os.path.exists(y_train_savepath) and os.path.exists(
        x_test_savepath) and os.path.exists(y_test_savepath):
    print('-------------Load Datasets-----------------')
    x_train_save = np.load(x_train_savepath, allow_pickle=True)
    y_train = np.load(y_train_savepath, allow_pickle=True)
    x_test_save = np.load(x_test_savepath, allow_pickle=True)
    y_test = np.load(y_test_savepath, allow_pickle=True)
    x_train = np.reshape(x_train_save, (len(x_train_save), 150, 150, 1))
    x_test = np.reshape(x_test_save, (len(x_test_save), 150, 150, 1))

else:
    print('-------------Generate Datasets-----------------')
    x_train, y_train = generateds(train_path, train_txt)
    x_test, y_test = generateds(test_path, test_txt)

    print('-------------Save Datasets-----------------')
    x_train_save = np.reshape(x_train, (len(x_train), -1))
    x_test_save = np.reshape(x_test, (len(x_test), -1))
    np.save(x_train_savepath, x_train_save)
    np.save(y_train_savepath, y_train)
    np.save(x_test_savepath, x_test_save)
    np.save(y_test_savepath, y_test)


# 这是第一种方法
# model = tf.keras.models.Sequential([
#     tf.keras.layers.Flatten(),
#     tf.keras.layers.Dense(512, activation='relu'),
#     tf.keras.layers.Dense(3, activation='softmax')
# ])

# Alexnet网络（这是第二种方法）待改进

# class AlexNet8(Model):
#     def __init__(self):
#         super(AlexNet8, self).__init__()
#
#         self.c1 = Conv2D(filters=96, kernel_size=(3, 3))
#         self.b1 = BatchNormalization()
#         self.a1 = Activation('relu')
#         self.p1 = MaxPool2D(pool_size=(3, 3), strides=2)
#
#         self.c2 = Conv2D(filters=256, kernel_size=(3, 3))
#         self.b2 = BatchNormalization()
#         self.a2 = Activation('relu')
#         self.p2 = MaxPool2D(pool_size=(3, 3), strides=2)
#
#         self.c3 = Conv2D(filters=384, kernel_size=(3, 3), padding='same',
#                          activation='relu')
#
#         self.c4 = Conv2D(filters=384, kernel_size=(3, 3), padding='same',
#                          activation='relu')
#
#         self.c5 = Conv2D(filters=256, kernel_size=(3, 3), padding='same',
#                          activation='relu')
#         self.p3 = MaxPool2D(pool_size=(3, 3), strides=2)
#
#         self.flatten = Flatten()
#         self.f1 = Dense(1024, activation='relu')
#         self.d1 = Dropout(0.5)
#         self.f2 = Dense(512, activation='relu')
#         self.d2 = Dropout(0.5)
#         self.f3 = Dense(3, activation='softmax')
#
#     def call(self, x):
#         x = self.c1(x)
#         x = self.b1(x)
#         x = self.a1(x)
#         x = self.p1(x)
#
#         x = self.c2(x)
#         x = self.b2(x)
#         x = self.a2(x)
#         x = self.p2(x)
#
#         x = self.c3(x)
#
#         x = self.c4(x)
#
#         x = self.c5(x)
#         x = self.p3(x)
#
#         x = self.flatten(x)
#         x = self.f1(x)
#         x = self.d1(x)
#         x = self.f2(x)
#         x = self.d2(x)
#         y = self.f3(x)
#         return y
# model = AlexNet8()


# 第三种方法（待改进）
model = tf.keras.models.Sequential([
    Conv2D(8, (5, 5), activation='relu', input_shape=(150, 150,1)),
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


model.compile(optimizer=tf.keras.optimizers.SGD(learning_rate=0.001),
              loss=tf.keras.losses.SparseCategoricalCrossentropy(),
              metrics=['accuracy'])

# model.compile(optimizer=RMSprop(lr=0.001), loss='binary_crossentropy', metrics=['acc'])

# 保存模型
checkpoint_save_path = "./checkpoint/my_model.ckpt"
if os.path.exists(checkpoint_save_path + '.index'):
    print('-------------load the model-----------------')
    model.load_weights(checkpoint_save_path,)

cp_callback = tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_save_path,
                                                 save_weights_only=True,
                                                 save_best_only=True)

history = model.fit(x_train, y_train, batch_size=8, epochs=100, validation_data=(x_test, y_test), validation_freq=1,
                    callbacks=[cp_callback])
model.summary()

###############################################    show   ###############################################

# 显示训练集和验证集的acc和loss曲线

acc = history.history['accuracy']
val_acc = history.history['val_accuracy']
loss = history.history['loss']
val_loss = history.history['val_loss']

plt.subplot(1, 2, 1)
plt.plot(acc, label='Training Accuracy')
plt.plot(val_acc, label='Validation Accuracy')
plt.title('Training and Validation Accuracy')
plt.legend()
plt.savefig('./Training_Accuracy.jpg')

plt.subplot(1, 2, 2)
plt.plot(loss, label='Training Loss')
plt.plot(val_loss, label='Validation Loss')
plt.title('Training and Validation Loss')
plt.legend()
plt.savefig('./Training_Loss.jpg')

plt.show()
