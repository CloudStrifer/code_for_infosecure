import csv
import os
import pandas as pd
from pathlib import Path
from prefix import PREFIX_TO_TRAFFIC_ID, ID_TO_TRAFFIC
import numpy as np

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


if __name__ == '__main__':
    csv_path = Path("../datasets/flows")   #csv文件路劲
    for csv_file in os.listdir(csv_path):   #针对每个csv文件，循环处理
        data = []
        label = []
        df = pd.read_csv("../datasets/flows/" + csv_file)
        #删除多余特征
        df = del_redundant_feature(df)
        df = standard_unit(df)
        df = add_label(df, csv_file)
        print(df)
        #输出处理好的文件
        df.to_csv("../datasets/flows_new/" + csv_file)

        # data.append(df[:])
        # label.append(df['label'])
        # data = np.array(data)
        # label = np.array(label)
        # np.savez("../datasets/flows_npz/" + csv_file, data=data, label=label)

        print("")