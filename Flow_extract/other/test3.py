import scapy
import numpy as np

# 打开pcap文件
from scapy.layers.inet import IP, TCP
from scapy.layers.l2 import Ether

cap = scapy.rdpcap("test.pcap")

# 定义每个数据包的最大长度
max_length = 100

# 定义一个空的numpy数组，用于存储所有数据包的bytes数据
data = np.zeros((len(cap), max_length), dtype=np.float32)

# 循环读取每个数据包
for i, packet in enumerate(cap):
    # 解析以太网首部
    eth_header = bytes(packet[Ether])
    # 解析IP首部
    ip_header = bytes(packet[IP])
    # 解析TCP首部
    tcp_header = bytes(packet[TCP])
    # 解析以太网尾部
    eth_trailer = bytes(packet[Ether].payload.payload.payload.payload)
    # 将所有bytes数据拼接起来
    raw_data = eth_header + ip_header + tcp_header + eth_trailer
    # 将bytes数据填充到100bytes范围
    padded_data = raw_data[:max_length].ljust(max_length, b'\x00')
    # 将bytes数据归一化到0-1范围
    normalized_data = np.frombuffer(padded_data, dtype=np.uint8) / 255.0
    # 将归一化后的数据存储到numpy数组中
    data[i] = normalized_data