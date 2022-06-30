from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris

# 载入鸢尾花数据
datas = load_iris()
X = datas.data
y = datas.target


#将鸢尾花数据集分为训练集和测试集
X_train,X_test,y_train,y_test = train_test_split(X,y,random_state=0)
#初始化分位数转化器
quantile_transformer = preprocessing.QuantileTransformer(random_state=0)
print(X_train)
#训练并转化数据
X_train_trans = quantile_transformer.fit_transform(X_train)
X_test_trans = quantile_transformer.fit_transform(X_test)
print(X_train_trans)


