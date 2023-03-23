import os

from nfstream import NFStreamer, NFPlugin
from pathlib import Path

def main():
    path_pcap = ("../datasets/pcap/")
    path_flows = ("../datasets/flows/")

    for pcap_file in os.listdir(path_pcap):
        my_awesome_streamer = NFStreamer(source=path_pcap + pcap_file, accounting_mode = 2, statistical_analysis=True, n_dissections=255,)  # or network interface (source="eth0")
        my_dataframe = my_awesome_streamer.to_pandas(columns_to_anonymize=[])
        #输出文件路径
        flows_save_path = path_flows +  pcap_file + '.csv'
        print(flows_save_path)
        #输出到csv文件
        my_awesome_streamer.to_csv(path=flows_save_path, columns_to_anonymize=[], flows_per_file=0, rotate_files=0)

if __name__ == "__main__":
    main()

