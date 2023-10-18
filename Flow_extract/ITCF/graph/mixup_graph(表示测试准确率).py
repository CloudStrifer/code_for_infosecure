import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties

# X坐标轴上的数字  
x_values = [2, 3, 4, 5, 6, 7, 8]

# Y坐标轴上的百分比  
y_values = [79.39, 86.63, 88.78, 89.26, 90.61, 85.25, 78.43]
font = FontProperties(fname=r"C:\Windows\Fonts\simsun.ttc", size=14) #设置字体
#plt.title("折线图示例", fontproperties=font) #使用字体
# 绘制二维折线图  
plt.plot(x_values, y_values, '-s', color='#FF7F0E')
plt.yticks(np.arange(50, 105, step=5))  #X轴刻度，范围是1到6，刻度为 1
plt.xticks(np.arange(2, 9, step=1))  #X轴刻度，范围是1到6，刻度为 1

# 设置X轴和Y轴的标签  
plt.xlabel('混合度λ', fontproperties=font)
plt.ylabel('准确率%', fontproperties=font)

# 设置图表标题  
#plt.title('数字与百分比')

# 显示图表  
plt.show()