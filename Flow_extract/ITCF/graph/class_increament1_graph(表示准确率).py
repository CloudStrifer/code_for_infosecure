import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties

# X坐标轴上的数字  
x_values = [1 , 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

# Y坐标轴上的百分比  
y_values = [94.4, 92.2, 90.2, 90.0, 89.4, 88.4, 86.2, 85.4, 85.2, 84.5, 83.4, 82.5]
font = FontProperties(fname=r"C:\Windows\Fonts\simsun.ttc", size=14) #设置字体
#plt.title("折线图示例", fontproperties=font) #使用字体
# 绘制二维折线图  
plt.plot(x_values, y_values, '-s', color='#FF7F0E')
plt.ylim(50,100) #将y轴的范围限制在20到30之间
plt.yticks(np.arange(50, 105, step=5))  #X轴刻度，范围是1到6，刻度为 1
plt.xticks(np.arange(0, 13, step=1))  #X轴刻度，范围是1到6，刻度为 1

# 设置X轴和Y轴的标签  
plt.xlabel('类数目', fontproperties=font)
plt.ylabel('准确率%', fontproperties=font)

# 设置图表标题  
#plt.title('数字与百分比')

# 显示图表  
plt.show()