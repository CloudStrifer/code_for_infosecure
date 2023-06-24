import matplotlib.pyplot as plt
import numpy as np
fig,axes = plt.subplots()
data_m = (40,120,20,100,30,200)
data_f = (60,180,30,150,20,50)
index = np.arange(6)
width = 0.4
axes.bar(index, data_m, width, color='c', label='men')
axes.bar(index+width, data_f, width, color='b', label='women')
axes.set_xticks(index+width/2)
axes.set_xticklabels(('a','b','c','d','e','f'))
axes.legend()
plt.show()
