import numpy as np
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris

# 载入鸢尾花数据
X = [[1,2,5,6],[8,0,21,22],[66,57,79,88]]


#初始化分位数转化器
quantile_transformer = preprocessing.QuantileTransformer(random_state=0)

#训练并转化数据
X_train = quantile_transformer.fit_transform(X)

print(np.percentile(X_train[:,0],[0,25,50,75,100]))


