# confusion_matrix
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.font_manager import FontProperties

classes = ['Youtube', 'Weibo', 'WeChat', 'Youku', 'Chrome', 'Email', 'QQ', 'P2P','Mail','FTPS']
confusion_matrix = np.array(
    [[94.8, 0,  0,  5,  0,   0,   0.2,  0,  0, 0],
     [0,  94.5,  2.5,  0,  3,   0,   0,    0,  0, 0],
     [0,  1,   99,  0,  0,   0,   0,    0,  0, 0],
     [0,  4.7, 1.2, 94.1, 0, 0,   0,    0,  0, 0],
     [0,  0,  0,  0,  100,  0,   1,  0,  0, 0],
     [0,  0,  0,  0,  0,   100,  0,  1,  2, 0],
     [0,  0,  0,  1.6,  0,   0,   98.4, 0, 0, 0],
     [0,  0,  0,  0,  0,   0,   0,  100, 0, 0],
     [0,  1,  0,  0,  0,   0,   0,  0, 99, 0],
     [0,  0,  0,  0.5,  0, 0, 6.8,  0 , 0, 92.7]
     ], dtype=int)  # 输入特征矩阵
proportion = []
length = len(confusion_matrix)
print(length)
for i in confusion_matrix:
    for j in i:
        temp = j / (np.sum(i))
        proportion.append(temp)
# print(np.sum(confusion_matrix[0]))
# print(proportion)
pshow = []
for i in proportion:
    pt = "%.2f%%" % (i * 100)
    pshow.append(pt)
proportion = np.array(proportion).reshape(length, length)  # reshape(列的长度，行的长度)
pshow = np.array(pshow).reshape(length, length)
# print(pshow)
config = {
    "font.family": 'Times New Roman',  # 设置字体类型
}
rcParams.update(config)
plt.imshow(proportion, interpolation='nearest', cmap=plt.cm.Blues)  # 按照像素显示出矩阵
# (改变颜色：'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds','YlOrBr', 'YlOrRd',
# 'OrRd', 'PuRd', 'RdPu', 'BuPu','GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn')
# plt.title('confusion_matrix')
plt.colorbar()
tick_marks = np.arange(len(classes))
plt.xticks(tick_marks, classes, fontsize=10)
plt.yticks(tick_marks, classes, fontsize=10)

thresh = confusion_matrix.max() / 2.
# iters = [[i,j] for i in range(len(classes)) for j in range((classes))]

iters = np.reshape([[[i, j] for j in range(length)] for i in range(length)], (confusion_matrix.size, 2))
for i, j in iters:
    if (i == j):
        #plt.text(j, i - 0.12, format(confusion_matrix[i, j]), va='center', ha='center', fontsize=10, color='white',
        #         weight=5)  # 显示对应的数字
        plt.text(j, i + 0.12, pshow[i, j], va='center', ha='center', fontsize=10, color='white')
    else:
        #plt.text(j, i - 0.12, format(confusion_matrix[i, j]), va='center', ha='center', fontsize=10)  # 显示对应的数字
        plt.text(j, i + 0.12, pshow[i, j], va='center', ha='center', fontsize=10)

font = FontProperties(fname=r"C:\Windows\Fonts\simsun.ttc", size=14) #设置字体
plt.ylabel('真实值', fontproperties=font)
plt.xlabel('预测值', fontproperties=font)
plt.tight_layout()
plt.show()
# plt.savefig('混淆矩阵.png')


