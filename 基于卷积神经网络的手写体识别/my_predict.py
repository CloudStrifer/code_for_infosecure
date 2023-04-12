#新建文件my_predict.py，编写代码如下：
from keras.models import load_model
import numpy as np
import cv2
model = load_model('cnn_model.h5')
image = cv2.imread('4.png', 0)
img = cv2.imread('4.png', 0)
img =np.reshape(img,(1,28,28,1)).astype(bool).astype("float32")/255
my_proba=model.predict_proba(img)
my_predict = model.predict_classes(img)
print ('识别为：')
print(my_proba)
print (my_predict)

cv2.imshow("Image1", image)
cv2.waitKey(0)
