import os
import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import ast

#抽取其中某个文件的ip_size 和  transport_size，做散点图
def visual_graph_from_individual_file():
    csv_path = Path("../datasets/flows_new")
    for csv_file in os.listdir(csv_path):
        df = pd.read_csv("../datasets/flows_new/" + csv_file)
        print(csv_file)
        ip_sizes_all = []
        delta_time_all = []
        transport_size_all = []
        for index, row in df.iterrows():
            ip_size = ast.literal_eval(row['udps.ip_size'])  # 因为是array，所以用这个办法转成list
            delta_time = ast.literal_eval(row['udps.delta_time'])
            transport_size = ast.literal_eval(row['udps.transport_size'])
            for i in range(0, len(ip_size)):
                 ip_sizes_all.append(ip_size[i])
            for i in range(0, len(delta_time)):
                 delta_time_all.append(delta_time[i])
            for i in range(0, len(transport_size)):
                 transport_size_all.append(transport_size[i])

        # x = np.array(ip_sizes_all)
        y = np.array(delta_time_all)
        x = np.array(transport_size_all)
        plt.figure(figsize=(10, 8), dpi=80) #设置图片宽高和dpi
        plt.scatter(x, y)  # 画散点图
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文
        plt.rcParams['axes.unicode_minus'] = False
        plt.xlabel('传输层数据包大小', fontdict={'size': 16})
        plt.ylabel('数据包到达间隔时间', fontdict={'size': 16})
        plt.show()

#这里是读取所有csv文件，保存在一个df中，并显示
def visual_graph_from_all_file():
    csv_path = Path("../datasets/flows_new")
    df_tmp = []
    for csv_file in os.listdir(csv_path):
        df = pd.read_csv("../datasets/flows_new/" + csv_file)
        df_tmp.append(df)
        print(csv_file)
    df_all = pd.concat(df_tmp,axis=0,ignore_index=True)  #把所有csv文件读取出来，然后组合在一个df中
    ip_sizes_all = []
    delta_time_all = []
    transport_size_all = []
    payload_size_all = []
    for index, row in df.iterrows():
        ip_size = ast.literal_eval(row['udps.ip_size'])  # ip层数据包大小
        delta_time = ast.literal_eval(row['udps.delta_time'])  #数据包到达间隔时间
        transport_size = ast.literal_eval(row['udps.transport_size'])  #传输层数据包大小
        payload_size = ast.literal_eval(row['udps.payload_size']) #数据包有效大小
        for i in range(0, len(ip_size)):
            if(ip_size[i] > 2000):
                ip_size[i] = 2000
            ip_sizes_all.append(ip_size[i])
        for i in range(0, len(delta_time)):
            delta_time_all.append(delta_time[i])
        for i in range(0, len(transport_size)):
            if(transport_size[i] > 2000):
                 transport_size[i] = 2000
            transport_size_all.append(transport_size[i])
        for i in range(0, len(payload_size)):
            if(payload_size[i]>2000):
                 payload_size[i] = 2000
            payload_size_all.append(payload_size[i])
    print(ip_sizes_all)
    print(delta_time_all)
    print(transport_size_all)
    print(payload_size_all)
    x = np.array(delta_time_all)
    y = np.array(payload_size_all)
    #x = np.array(transport_size_all)
    plt.figure(figsize=(10,8),dpi=80) #设置图片宽高和dpi
    plt.scatter(x, y)  # 画散点图
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文
    plt.rcParams['axes.unicode_minus'] = False
    plt.xlabel('数据包到达间隔时间', fontdict={'size': 16})
    plt.ylabel('传输层数据包大小', fontdict={'size': 16})
    plt.show()

def visual_graph_from_all_file_flow():
    csv_path = Path("../datasets/flows_new")
    df_tmp = []
    for csv_file in os.listdir(csv_path):
        df = pd.read_csv("../datasets/flows_new/" + csv_file)
        df_tmp.append(df)
        print(csv_file)
    df_all = pd.concat(df_tmp, axis=0, ignore_index=True)  # 把所有csv文件读取出来，然后组合在一个df中
    bidirectional_duration_ms_all = []
    bidirectional_bytes_all = []

    for index, row in df.iterrows():
        bidirectional_duration_ms = row['bidirectional_duration_ms']
        bidirectional_bytes = row['bidirectional_bytes']
        if (bidirectional_bytes <= 2000):
            bidirectional_duration_ms_all.append(bidirectional_duration_ms)
            bidirectional_bytes_all.append(bidirectional_bytes)
    print(bidirectional_duration_ms_all)
    x = np.array(bidirectional_duration_ms_all)
    y = np.array(bidirectional_bytes_all)
    #x = np.array(transport_size_all)
    plt.figure(figsize=(10,8),dpi=80) #设置图片宽高和dpi
    plt.scatter(x, y)  # 画散点图
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文
    plt.rcParams['axes.unicode_minus'] = False
    plt.xlabel('数据包到达间隔时间', fontdict={'size': 16})
    plt.ylabel('传输层数据包大小', fontdict={'size': 16})
    plt.show()

if __name__ == '__main__':
    #visual_graph_from_individual_file()   #这个是单个文件中数据包为单位的绘图
    visual_graph_from_all_file()   # 这个是以数据包为单位的绘图
    #visual_graph_from_all_file_flow()  #这个是以流为单位的绘图




