import csv
import os
import tensorflow as tf
from keras import backend as K
# K.tensorflow_backend._get_available_gpus()
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import zscore
from math import radians, cos, sin, asin, sqrt
import seaborn as sns
import keras
from keras import metrics
from keras import regularizers
from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout, Flatten, Activation
from keras.optimizers import Adam, RMSprop
from keras.callbacks import TensorBoard, EarlyStopping, ModelCheckpoint
from keras.utils import plot_model
from sklearn.linear_model import Lasso, LogisticRegression
from sklearn.feature_selection import SelectFromModel
from sklearn.preprocessing import StandardScaler
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from keras.models import Sequential
from keras.layers import Dense
from keras import regularizers
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
import json
from prefix import PREFIX_TO_TRAFFIC_ID, ID_TO_TRAFFIC
import glob
from keras.layers import Conv2D, MaxPooling2D,AveragePooling2D


# 指定csv文件所在目录
path = 'E:/PyCharmCode/Flow_extract/ITCF/csv/'
batch_size = 128  # 批处理样本数量
input_shape = (28, 28,1)  # 输入图片的维度
i = 0
rows = 28
cols = 28

data_total = []
label_total = []
#循环读取csv文件
for filename in os.listdir(path):
    if filename.endswith('.csv'):
        sampled_data = pd.read_csv(path + filename, header=None)  #因为头部没有，所以不需要把头部当做列名
        df = pd.DataFrame(sampled_data)  #转换成df格式
        label_total.extend(df.iloc[:,-1].tolist())   #获取最右边的值
        df = df.drop(df.columns[-1], axis=1)  # 去掉最右边那一行

        for index, row in df.iterrows():    #一行一行的读取
            row_value = df.iloc[index].values     #获取当前的值
            tmp = row_value.reshape(rows, cols)
            tmp = tmp.tolist()       #转换成list类型
            data_total.append(tmp)   #将每一项添加到集合中


df_total = pd.DataFrame()
def train():
    data = np.array(data_total)
    labels = np.array(label_total)
    # y = np.full(len(sampled_df), label)
    # y = np.ravel(sampled_df['class'])
    y = labels
    x = data

    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
    X_train = X_train[:, :, :, np.newaxis]  # 添加一个维度，代表图片通道。这样数据集共4个维度，样本个数、宽度、高度、通道数
    X_test = X_test[:, :, :, np.newaxis]  # 添加一个维度，代表图片通道。这样数据集共4个维度，样本个数、宽度、高度、通道数
    print('样本数据集的维度：', X_train.shape, y_train.shape)
    print('测试数据集的维度：', X_test.shape, y_test.shape)

    # 定义模型
    model = Sequential()
    # 添加第一个卷积层
    model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)))
    model.add(MaxPooling2D((2, 2)))

    # 添加第二个卷积层
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D((2, 2)))

    # 添加第三个卷积层
    model.add(Conv2D(64, (3, 3), activation='relu'))

    # 添加全连接层
    model.add(Flatten())
    model.add(Dense(64, activation='relu'))
    model.add(Dense(10, activation='softmax'))

    # 编译模型
    model.compile(optimizer='adadelta',loss='SparseCategoricalCrossentropy',metrics=['accuracy'])
    model.summary()
    # 训练模型
    history = model.fit(X_train, y_train, epochs=100,verbose=1, validation_data=(X_test, y_test))

    # 评估模型
    score = model.evaluate(X_test, y_test, verbose=0)

    print('Test score:', score[0])
    print('Test accuracy:', score[1])
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    loss = history.history['loss']
    val_loss = history.history['val_loss']
    epochs = range(len(acc))

    plt.plot(epochs,acc, 'b', label='Training accuracy')
    plt.plot(epochs, val_acc, 'r', label='validation accuracy')
    plt.title('Training and validation accuracy')
    plt.legend(loc='lower right')
    plt.figure()

    plt.plot(epochs, loss, 'r', label='Training loss')
    plt.plot(epochs, val_loss, 'b', label='validation loss')
    plt.title('Training and validation loss')
    plt.legend()
    plt.show()

if __name__ == '__main__':
    train()