import os
import numpy as np
np.random.seed(1337)  # for reproducibility
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D,AveragePooling2D
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import os
from sklearn.model_selection import train_test_split
from prefix import PREFIX_TO_TRAFFIC_ID, ID_TO_TRAFFIC
import ast
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
# 全局变量
batch_size = 128  # 批处理样本数量
nb_classes = 10  # 分类数目
epochs = 600  # 迭代次数
img_rows, img_cols = 1500, 1500  # 输入图片样本的宽高
nb_filters = 32  # 卷积核的个数
pool_size = (2, 2)  # 池化层的大小
kernel_size = (50, 50)  # 卷积核的大小
input_shape = (img_rows, img_cols,1)  # 输入图片的维度

def get_training_data_set():
    csv_path = Path("../datasets/flows_new")
    flow_dataset = []
    flow_picture_labels = []
    for csv_file in os.listdir(csv_path):
        df = pd.read_csv("../datasets/flows_new/" + csv_file)
        print(csv_file)

        #先提取文件，然后对这个文件做行循环，每一行提取其udps.time和udps.size这2个列里面的数据，放到1500x1500的二维矩阵中，组成一个list[[],[],[]]
        for index, row in df.iterrows():
            flow_picture_data = [[0 for _ in range(1500)] for _ in range(1500)] #创建1500x1500的二维矩阵
            flow_picture_label = []
            time = ast.literal_eval(row['udps.time'])  #返回list类型
            size = ast.literal_eval(row['udps.size'])  #返回list类型
            for i in range(len(time)):  #因为x和y数据长度是一样的，所以循环其中一个就可以了
                if (time[i] < 1500 and size[i] < 1500): #接着把这个数据放到二维list列表里,其实就是组建一个二维流图
                    flow_picture_data[time[i]][size[i]] = 1
                    label = row['label']
            flow_dataset.append(flow_picture_data)   #当前这一行的数据填充好以后，就放入集合里
            flow_picture_labels.append(row['label'])
        print("hehe")

    return flow_dataset, flow_picture_labels   # 图片为[[x,x,x..][x,x,x...][x,x,x...][x,x,x...]]的列表

datasets, labels = get_training_data_set()

#划分训练集和测试集
X_train, X_test, Y_train, Y_test = train_test_split(
    datasets, labels, test_size=0.30, random_state=42)

#X_train = datasets
#Y_train = labels

#X_test = datasets
#Y_test = labels

#X_train = np.array(X_train).astype(bool).astype(float)/255    #数据归一化
X_train = np.array(X_train)
X_train = X_train[:,:,:,np.newaxis]  # 添加一个维度，代表图片通道。这样数据集共4个维度，样本个数、宽度、高度、通道数
Y_train = np.array(Y_train)
#X_test = np.array(X_test).astype(bool).astype(float)/255    #数据归一化
X_test = np.array(X_test)
X_test = X_test[:,:,:,np.newaxis]  # 添加一个维度，代表图片通道。这样数据集共4个维度，样本个数、宽度、高度、通道数
Y_test = np.array(Y_test)
print('样本数据集的维度：', X_train.shape,Y_train.shape)
print('测试数据集的维度：', X_test.shape,Y_test.shape)

# 构建模型
model = Sequential()
model.add(Conv2D(10,(10,10),input_shape=input_shape, padding='same', strides=5))  # 卷积层1
#model.add(AveragePooling2D(pool_size=(150,150),strides=2))  # 池化层
model.add(MaxPooling2D(150,strides=1)) #池化层1
model.add(Conv2D(20,(10,10),padding='same', strides=5))  # 卷积层2
#model.add(AveragePooling2D(pool_size=(150,150),strides=2))  # 池化层
model.add(MaxPooling2D(15,strides=1)) #池化层2
model.add(Flatten())  # 拉成一维数据
model.add(Dense(10))  # 全连接层2
model.add(Activation('softmax'))  # sigmoid评分
model.summary()
# 编译模型
model.compile(loss='SparseCategoricalCrossentropy',optimizer='adadelta',metrics=['accuracy'])
# 训练模型
history = model.fit(X_train, Y_train, batch_size=batch_size, epochs=5,verbose=1, validation_data=(X_test, Y_test))
# 评估模型
score = model.evaluate(X_test, Y_test, verbose=0)
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
#plt.savefig("accuracy_loss.jpg")
#os.system("pause")
# 保存模型
#model.save('cnn_model.h5')   # HDF5文件, pip install h5py

