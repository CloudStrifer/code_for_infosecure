import pandas as pd

import csv

import scapy
import numpy as np
import os
# 打开pcap文件
from scapy.layers.inet import IP, TCP
from scapy.layers.l2 import Ether
from prefix import PREFIX_TO_TRAFFIC_ID, ID_TO_TRAFFIC

def compute_packet_head(folder_path, filename):
    cap = scapy.utils.rdpcap(os.path.join(folder_path, filename))
    # 定义每个数据包的最大长度
    max_length = 150
    # 定义一个空的numpy数组，用于存储所有数据包的bytes数据
    data = np.zeros((len(cap), max_length), dtype=np.float32)
    # 循环读取每个数据包
    for i, packet in enumerate(cap):
        # 填充值
        padding = b'\x00'
        # 解析以太网首部
        eth_header = b'\x00'
        if Ether in packet:
            eth_header = bytes(packet[Ether])
        # 解析IP首部
        ip_header = b'\x00'
        if (IP in packet):
            ip_header = bytes(packet[IP])
            # 清楚掉源和目的IP地址
            packet[IP].src = '0.0.0.0'
            packet[IP].dst = '0.0.0.0'
            # 通过ttl值判断方向，如果是出口方向，那么肯定是原始的，由于linux，window默认的不太一样，所以把这几种情况都列上
            if (packet[IP].ttl == 64 or packet[IP].ttl == 128 or packet[IP].ttl == 255 or packet[IP].ttl == 1):
                padding = b'\x00'  # 如果是源到目的，则填充0(十进制)
            else:
                padding = b'\xF0'  # 如果是目的到源，则填充240(十进制)
        # 解析TCP首部
        tcp_header = b'\x00'
        if (TCP in packet):
            tcp_header = bytes(packet[TCP])

        # 将所有bytes数据拼接起来
        raw_data = eth_header + ip_header + tcp_header
        # 将bytes数据填充到100bytes范围
        padded_data = raw_data[:max_length].ljust(max_length, padding)
        # 将bytes数据归一化到0-1范围
        normalized_data = np.frombuffer(padded_data, dtype=np.uint8) / 255.0
        # 将归一化后的数据存储到numpy数组中
        data[i] = normalized_data
    print(len(data))
    #print(data)
    return data

def new_csv(data, filename):
    path = 'E:/PyCharmCode/Flow_extract/FFEM/csv/'
    filename = filename + '.csv'
    print(data)
    df = pd.DataFrame(data)
    csv_file_prefix = filename.lower()[:-4]
    labels = PREFIX_TO_TRAFFIC_ID.get(csv_file_prefix)
    df[len(df.columns)] = labels        #在最右边添加一列
    data = df.values            #将df转换成ndarray

    # 新建csv文件
    with open(path + filename, 'w', newline='') as csvfile:  #给文件最右侧添加标签


        # 创建csv写入器
        writer = csv.writer(csvfile)
        # 写入数据
        for row in data:
            writer.writerow(row)


if __name__ == '__main__':
    # 指定文件夹路径
    folder_path = 'E:\PyCharmCode\Flow_extract\FFEM\pcap'
    # 遍历文件夹下的所有文件
    for filename in os.listdir(folder_path):
        # 判断文件是否为pcap文件
        if filename.endswith('.pcap'):
            data = compute_packet_head(folder_path, filename)
            new_csv(data, filename[:-5])  #去掉最后的pcap文件名