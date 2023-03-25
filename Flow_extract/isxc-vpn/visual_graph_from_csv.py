import os
import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt


if __name__ == '__main__':
    csv_path = Path("../datasets/flows_new")
    for csv_file in os.listdir(csv_path):
         df = pd.read_csv("../datasets/flows_new/" + csv_file)
         print(csv_file)
         plt.scatter(df['bidirectional_mean_ps'],df['bidirectional_duration_ms']) #画散点图
         plt.show()



