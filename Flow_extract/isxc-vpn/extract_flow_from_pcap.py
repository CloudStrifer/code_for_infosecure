import os

from nfstream import NFStreamer, NFPlugin
from pathlib import Path

class Extend_Add_Time_Size(NFPlugin):

    # 通过扩展方法，将传输层数据大小和包达到时间（单位是毫秒）保存在list列表中
    def on_init(self, packet, flow):
        flow.udps.size = []
        flow.udps.size.append(packet.transport_size)

        flow.udps.time = []
        flow.udps.time.append(flow.bidirectional_first_seen_ms) #为了保证后面计算的时候，x和y轴数字个数相同，所以先把双向流第一个时间放进来，其实第一个包减去
        #双向流第一个时间，基本都是0
        flow.udps.time.append(packet.time)

    def on_update(self, packet, flow):
        #为了防止有的数据太大，导致填满，所以采取这种办法
        if(len(flow.udps.size)<1000) :
              flow.udps.size.append(packet.transport_size)
              flow.udps.time.append(packet.time)


def main():
    path_pcap = ("../datasets/pcap/")     #pcap流量文件路劲
    path_flows = ("../datasets/flows/")   #输出后csv文件路劲

    for pcap_file in os.listdir(path_pcap):
        my_awesome_streamer = NFStreamer(source=path_pcap + pcap_file, accounting_mode = 2, statistical_analysis=True, n_dissections=255,
                                         udps=Extend_Add_Time_Size())  # or network interface (source="eth0")
        my_dataframe = my_awesome_streamer.to_pandas(columns_to_anonymize=[])
        #输出文件路径
        flows_save_path = path_flows +  pcap_file + '.csv'
        print(flows_save_path)
        #输出到csv文件
        my_awesome_streamer.to_csv(path=flows_save_path, columns_to_anonymize=[], flows_per_file=0, rotate_files=0)

if __name__ == "__main__":
    main()

