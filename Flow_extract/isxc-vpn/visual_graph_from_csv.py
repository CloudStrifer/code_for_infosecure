import os
import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from keras.models import Sequential, load_model
import ast

# 抽取其中某个文件的bidirectional_mean_ps 和  bidirectional_duration_ms，做散点图
if __name__ == '__main__':
    csv_path = Path("../datasets/flows_new")
    for csv_file in os.listdir(csv_path):
         df = pd.read_csv("../datasets/flows_new/" + csv_file)
         print(csv_file)
         sizes = []
         times = []
         for index, row in df.iterrows():
             size = ast.literal_eval(row['udps.size'])  # 因为是array，所以用这个办法转成list
             time = ast.literal_eval(row['udps.time']) # 本来就是list了，就不用特意转成List
             for i in range(0,len(size)):
                 sizes.append(size[i])
             for i in range(0,len(time)):
                 times.append(time[i])

         x = np.array(sizes)
         y = np.array(times)
         plt.scatter(x,y) #画散点图
         plt.show()



