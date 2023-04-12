import os
import numpy as np
np.random.seed(1337)  # for reproducibility
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D,AveragePooling2D
from pathlib import Path
import pandas as pd
from prefix import PREFIX_TO_TRAFFIC_ID, ID_TO_TRAFFIC
# 全局变量
batch_size = 128  # 批处理样本数量
nb_classes = 10  # 分类数目
epochs = 600  # 迭代次数
img_rows, img_cols = 2000, 2000  # 输入图片样本的宽高
nb_filters = 32  # 卷积核的个数
pool_size = (2, 2)  # 池化层的大小
kernel_size = (50, 50)  # 卷积核的大小
input_shape = (img_rows, img_cols,1)  # 输入图片的维度

def get_training_data_set():
    csv_path = Path("../datasets/flows_new")
    flow_dataset = []
    flow_picture_label = []
    for csv_file in os.listdir(csv_path):
        df = pd.read_csv("../datasets/flows_new/" + csv_file)
        print(csv_file)
        # 这里设置宽和高都为2000，这样基本能把所有数据的点给采集到
        row, col = 2000, 2000
        flow_picture_data = [[0 for _ in range(col)] for _ in range(row)] #创建一个二维列表，其宽高均为2000

        for i in range(len(df)):
                bidirectional_mean_ps = int(df.at[i,'bidirectional_mean_ps']) #获取其中df对应的值
                bidirectional_duration_ms = int(df.at[i,'bidirectional_duration_ms'])
                #if (bidirectional_mean_ps < 1500 and bidirectional_duration_ms < 1500): #之前测试是在1500以内，现在改成2000了
                flow_picture_data[bidirectional_mean_ps][bidirectional_duration_ms] = 1
        #获取该流量的文件类型名字
        csv_file_prefix = csv_file.lower()[:-9]
        labels = PREFIX_TO_TRAFFIC_ID.get(csv_file_prefix)

        #把刚获取到的数据和标签放入list集合中，在这里
        flow_dataset.append(flow_picture_data)
        flow_picture_label.append(labels)

    return flow_dataset, flow_picture_label   # 图片为[[x,x,x..][x,x,x...][x,x,x...][x,x,x...]]的列表

#这里的方法，是通过获取1个csv文件，把所有数据的点全部放在一个集合中，意思也就是1个pcap文件，代表一种类型，它就有一个流图
datasets, labels = get_training_data_set()


# X_train, Y_train = MNIST.get_training_data_set(600, False)  # 加载训练样本数据集，和one-hot编码后的样本标签数据集。最大60000
# X_test, Y_test = MNIST.get_test_data_set(100, False)  # 加载测试特征数据集，和one-hot编码后的测试标签数据集，最大10000
X_train = datasets
Y_train = labels

X_test = datasets
Y_test = labels

X_train = np.array(X_train).astype(bool).astype(float)/255    #数据归一化
X_train=X_train[:,:,:,np.newaxis]  # 添加一个维度，代表图片通道。这样数据集共4个维度，样本个数、宽度、高度、通道数
Y_train = np.array(Y_train)
X_test = np.array(X_test).astype(bool).astype(float)/255    #数据归一化
X_test=X_test[:,:,:,np.newaxis]  # 添加一个维度，代表图片通道。这样数据集共4个维度，样本个数、宽度、高度、通道数
Y_test = np.array(Y_test)
print('样本数据集的维度：', X_train.shape,Y_train.shape)
print('测试数据集的维度：', X_test.shape,Y_test.shape)

# 构建模型，目前用的是AlexNet模型，自己修改了卷积层和池化层的参数和步长等信息
model = Sequential()
model.add(Conv2D(10,(10,10),input_shape=input_shape,padding ='same',strides=2))  # 卷积层1
model.add(Activation("relu"))
model.add(MaxPooling2D(pool_size=(200,200),strides=1)) #池化层1
model.add(Conv2D(20,(20,20),padding ='same',strides=2))  # 卷积层2
model.add(Activation("relu"))
model.add(MaxPooling2D(pool_size=(100,100),strides=1))  # 池化层2
model.add(Conv2D(20,(5,5),padding ='same',strides=1))  # 卷积层3
model.add(Activation("relu"))
model.add(Conv2D(20,(10,10),padding ='same',strides=2))  # 卷积层4
model.add(Activation("relu"))
model.add(Conv2D(20,(10,10),padding ='same',strides=2))  # 卷积层5
model.add(Activation("relu"))
model.add(MaxPooling2D(pool_size=(25,25),strides=2))  # 池化层3
model.add(Flatten())  # 拉成一维数据
model.add(Dense(64))  # 全连接层2
model.add(Activation('softmax'))  # sigmoid评分
model.summary()  #显示每层输出参数

# 编译模型
model.compile(loss='SparseCategoricalCrossentropy',optimizer='adadelta',metrics=['accuracy'])
# 训练模型
model.fit(X_train, Y_train, batch_size=batch_size, epochs=5,verbose=1, validation_data=(X_test, Y_test))
# 评估模型
score = model.evaluate(X_test, Y_test, verbose=0)
print('Test score:', score[0])
print('Test accuracy:', score[1])
# 保存模型
model.save('cnn_model.h5')   # HDF5文件, pip install h5py
