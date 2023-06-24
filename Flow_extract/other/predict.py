import os;
import glob;
import sys
import numpy as np
import scipy.ndimage as ndimage
from tqdm import tqdm, trange
import matplotlib.pyplot as plt


def multi_hist(data, title="hospital_patient", xlabel="hospitals", ylabel="patients", bins=16):
    # data : shape = M*N
    # assert len(np.shape(data))==2, r"数据要二维度的"
    title = r"Histogram with '{}' bins".format(title)
    xlabel = r"{}_({})".format(xlabel, "M")
    ylabel = r"{}_({})".format(ylabel, "M")
    num = len(data)
    label = [r"bar. - {}".format(str(i)) for i in range(num)]
    color = [j for i, j in zip(range(num), ['r', 'g', 'b', 'y'])]
    plt.hist(  ## 绘制数据直方图
        x=data,  # 输入数据 - 自动统计相同元素出现的数量
        bins=bins,  # 指定直方图的条形数为20个
        edgecolor='w',  # 指定直方图的边框色
        color=color,  # 指定直方图的填充色
        label=label,  # 为直方图呈现图例
        density=False,  # 是否将纵轴设置为密度，即频率
        alpha=0.8,  # 透明度
        rwidth=1,  # 直方图宽度百分比：0-1
        stacked=True)  # 当有多个数据时，是否需要将直方图呈堆叠摆放，默认水平摆放
    # 显示图例
    plt.title(label=title)
    plt.xlabel(xlabel=xlabel)
    plt.ylabel(ylabel=ylabel)
    plt.legend()
    # 显示图形
    plt.show()
    pass


sample1 = [0, 0, 0, 1, 2, 2, 4, 5, 3, 6, 6, 6, 6, 6, 10, 10, 10, 15, 15]
sample2 = [0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 9]
data = [sample1, sample2]
multi_hist(data, title="hospital_patient", xlabel="hospitals", ylabel="patients")