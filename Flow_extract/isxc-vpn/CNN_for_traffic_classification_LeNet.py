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
    flow_picture_label = []
    for csv_file in os.listdir(csv_path):
        df = pd.read_csv("../datasets/flows_new/" + csv_file)
        print(csv_file)

        row, col = 1500, 1500
        flow_picture_data = [[0 for _ in range(col)] for _ in range(row)]

        for i in range(len(df)):
                bidirectional_mean_ps = int(df.at[i,'bidirectional_mean_ps'])
                bidirectional_duration_ms = int(df.at[i,'bidirectional_duration_ms'])
                if (bidirectional_mean_ps < 1500 and bidirectional_duration_ms < 1500):
                    flow_picture_data[bidirectional_mean_ps][bidirectional_duration_ms] = 1

        csv_file_prefix = csv_file.lower()[:-9]
        labels = PREFIX_TO_TRAFFIC_ID.get(csv_file_prefix)

        flow_dataset.append(flow_picture_data)
        flow_picture_label.append(labels)

    return flow_dataset, flow_picture_label   # 图片为[[x,x,x..][x,x,x...][x,x,x...][x,x,x...]]的列表

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
model.add(Dense(64))  # 全连接层2
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

