import matplotlib.pyplot as plt
import numpy as np
from matplotlib.font_manager import FontProperties

# X坐标轴上的数字  
x_values_mix_icarl = [2 , 4, 6 , 8,  10, 12]
# Y坐标轴上的百分比
y_values_mix_icarl = [91.8, 89.2 , 87.5, 84.5, 82.1, 79.9]

x_values_icarl = [2 , 4, 6 , 8,  10, 12]
y_values_icarl = [90.4, 85.5 , 82.3, 78.4, 77.1, 75.9]

x_values_lwf = [2 , 4, 6 , 8,  10, 12]
y_values_lwf = [89.2, 80.1 , 75.3, 70.4, 68.1, 64.9]

x_values_fine = [2 , 4, 6 , 8,  10, 12]
y_values_fine = [89.6, 82.1 , 73.5, 68.4, 65.1, 61.8]


font = FontProperties(fname=r"C:\Windows\Fonts\simsun.ttc", size=14) #设置字体
#plt.title("折线图示例", fontproperties=font) #使用字体
# 绘制二维折线图  
plt.plot(x_values_mix_icarl, y_values_mix_icarl, '-s', color='#FF7F0E')
plt.plot(x_values_icarl, y_values_icarl, "-s", color='blue')
plt.plot(x_values_lwf,y_values_lwf, "-s", color='green')
plt.plot(x_values_fine,y_values_fine, "-s", color='red')
plt.legend(['Mixup_iCaRL','iCaRL','LWF','FineTune'])

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