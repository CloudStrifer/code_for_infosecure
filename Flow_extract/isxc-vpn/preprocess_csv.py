import csv
import math
import os
import pandas as pd
from pathlib import Path
from prefix import PREFIX_TO_TRAFFIC_ID, ID_TO_TRAFFIC
import numpy as np
import ast

from sklearn import preprocessing

# 删除多余特征
def del_redundant_feature(df):
    df = df.drop(['id','expiration_id','src_mac','src_oui','dst_mac','dst_oui','vlan_id',
                  'tunnel_id','bidirectional_first_seen_ms','bidirectional_last_seen_ms','src2dst_first_seen_ms','bidirectional_min_ps',
                  'bidirectional_stddev_ps','bidirectional_max_ps', 'src2dst_last_seen_ms','src2dst_duration_ms','src2dst_packets','src2dst_bytes', 'dst2src_first_seen_ms','dst2src_last_seen_ms','dst2src_duration_ms',
                  'dst2src_packets','dst2src_bytes','src2dst_min_ps','src2dst_mean_ps','src2dst_stddev_ps','src2dst_max_ps',
                  'dst2src_min_ps','dst2src_mean_ps','dst2src_stddev_ps','dst2src_max_ps','bidirectional_min_piat_ms',
                   'bidirectional_stddev_piat_ms','bidirectional_max_piat_ms',
                  'src2dst_min_piat_ms','src2dst_mean_piat_ms','src2dst_stddev_piat_ms','src2dst_max_piat_ms','dst2src_min_piat_ms',
                  'dst2src_mean_piat_ms','dst2src_stddev_piat_ms','dst2src_max_piat_ms','src2dst_syn_packets','src2dst_cwr_packets',
                  'src2dst_ece_packets', 'src2dst_urg_packets','src2dst_ack_packets','src2dst_psh_packets','src2dst_rst_packets',
                  'src2dst_fin_packets','dst2src_syn_packets','dst2src_cwr_packets'	,'dst2src_ece_packets','dst2src_urg_packets',
                  'dst2src_ack_packets','dst2src_psh_packets','dst2src_rst_packets'	,'dst2src_fin_packets',
                  'application_is_guessed','application_confidence','requested_server_name','client_fingerprint'
                  ,'server_fingerprint','user_agent','content_type',], axis=1)  # 删除多余的列
    return df

#标准化单位。需要统一标准的有不少，首先是时间，除以1000,得到单位为s
#其次是bytes字节数，除以1024，得到单位是Kb
def standard_unit(df):
    df['bidirectional_duration_ms'] = df['bidirectional_duration_ms'] / 1000   #之前该时间的单位是毫秒, 流双向持续时间
    df['bidirectional_mean_piat_ms'] = df['bidirectional_mean_piat_ms'] / 1000  # 流双向平均数据包到达间隔时间。
    #df['bidirectional_bytes'] = df['bidirectional_bytes'] / 1024   #之前该单位是位

    return df


#根据prefix.py文件中的标签，对不同文件做标记，数字为0-9
#其中0: 'Chat',1: 'Email',2: 'File Transfer',3: 'Streaming', 4: 'Voip', 5: 'VPN: Chat', 6: 'VPN: File Transfer', 7: 'VPN: Email',
# 8: 'VPN: Streaming', 9: 'VPN: Voip',
def add_label(df, csv_file):
    csv_file_prefix = csv_file.lower()[:-9]
    df['label'] = PREFIX_TO_TRAFFIC_ID.get(csv_file_prefix)
    return df


#删除无用的流数据，主要是一些ICMP，DHCPV6这些流(目前暂时不管，后面再说吧）
#还有一些流udps.size只有1个，也就是说它只有一个包，这种流用处也不大，删除
#目前还删了udps.time只有1个或者为0的，这种意义也不大，删除
#按行遍历
def del_useless_flow(df):
    for index,row in df.iterrows():
        size = ast.literal_eval(row['udps.size'])          #因为是array，所以用这个办法转成list
        time = row['udps.time']   #本来就是list了，就不用特意转成List
        if (len(size)<=1 or len(time) <=1) :
            df = df.drop(index)
    return df


#计算到达间隔时间
#也就是计算每一个时间和第一个时间的间隔
def count_inter_time(df):
    for index,row in df.iterrows():
        time = ast.literal_eval(row['udps.time'])  #由于返回的是list,只能用这个办法才可以获取得到
        inter_time_list = []
        for i in range(len(time)-1):
            inter_time = time[i+1] - time[i]   #将时间间隔提取出来，做一个新的list
            inter_time = inter_time / 1000
            inter_time_list.append(inter_time)
        # 判断是否间隔大于1个，这样方便进行时间间隔的标准化，将其范围扩展到0-1500之间
        if (len(inter_time_list) > 1 ):
            inter_time_list = list(rescale_linear(np.array(inter_time_list),0,1500))
            inter_time_list = list(map(int, inter_time_list[:]))   #对里面的元素取整，保证后面计算方便
        row['udps.time'] = inter_time_list
        df.iloc[index] = row
    return df

#后面可能要改哦
#网上找来的代码，就是扩展一维数据范围的，能用就行，不用管
def rescale_linear(array, new_min, new_max):
    """Rescale an arrary linearly."""
    minimum, maximum = np.min(array), np.max(array)
    if ((maximum-minimum)==0):         #如果时间间隔都是0，则创建一个为0的数组，然后返回回去
        lens = len(array)
        return np.zeros(lens)
    m = int((new_max - new_min) / (maximum - minimum))
    b = new_min - m * minimum
    return m * array + b

if __name__ == '__main__':
    csv_path = Path("../datasets/flows")   #csv文件路劲
    for csv_file in os.listdir(csv_path):   #针对每个csv文件，循环处理
        data = []
        label = []
        df = pd.read_csv("../datasets/flows/" + csv_file)
        #删除多余特征
        df = del_redundant_feature(df)
        df = standard_unit(df)
        df = count_inter_time(df)      #这个顺序必须在del_useless_flow方法前面，切记
        df = del_useless_flow(df)
        df = add_label(df, csv_file)
        print(df)
        #输出处理好的文件
        df.to_csv("../datasets/flows_new/" + csv_file)
