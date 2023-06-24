import csv
import os
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
# 指定csv文件所在目录
path = 'E:/PyCharmCode/Flow_extract/FFEM/csv/'
df_total = pd.DataFrame()

#循环读取csv文件
for filename in os.listdir(path):
    if filename.endswith('.csv'):
        sampled_data = pd.read_csv(path + filename, header=None)  #因为头部没有，所以不需要把头部当做列名
        sampled_data = pd.DataFrame(sampled_data)
        df_total = pd.concat([df_total, sampled_data])
        print("1")



def train():
    # y = np.full(len(sampled_df), label)
    # y = np.ravel(sampled_df['class'])
    y = df_total.iloc[:,-1]  #获取最右边一列
    x = df_total.drop(df_total.columns[-1],axis=1) #把最右边那列去掉

    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

    # Scaling the inputs
    scaler = StandardScaler().fit(X_train)
    X_train = scaler.transform(X_train)
    X_test = scaler.transform(X_test)

    # Defining the model
    model = Sequential()
    model.add(Dense(32, activation='relu', input_shape=(150,)))
    model.add(Dropout(0.1))
    model.add(Dense(16, activation='relu'))
    model.add(Dense(11, activation='softmax'))
    # Model Summary
    model.summary();

    # Training the model
    model.compile(loss='sparse_categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])

    history = model.fit(X_train, y_train, epochs=50, batch_size=32, verbose=1, validation_data=(X_test, y_test))
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