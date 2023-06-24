import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import MultipleLocator

fig,axes = plt.subplots()
data_m = (0.97,0.98,0.94,0.98,0.84,0.93)
data_f = (0.94,0.95,0.99,0.98,0.91,0.90)
index = np.arange(6)
width = 0.4

axes.bar(index, data_m, width, color='c', label='精准率')
axes.bar(index+width, data_f, width, color='b', label='召回率')
axes.set_xticks(index+width/2)
axes.set_xticklabels(('实验一\n(数据包层面)','实验一\n(流层面)','实验二\n(数据包层面)','实验二\n(流层面)','实验三\n(数据包层面)','实验三\n(流层面)'))
y_major_locator = MultipleLocator(0.05)  #把y轴的刻度间隔设置为0.05，并存在变量里
axes.yaxis.set_major_locator(y_major_locator)
axes.legend()
plt.ylim(0.80,1.00)
plt.rcParams['font.sans-serif']=['SimHei'] # 用来正常显示中文标签（中文乱码问题）
plt.show()
