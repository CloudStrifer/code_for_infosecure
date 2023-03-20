from nfstream import NFStreamer, NFPlugin
from Simhash import Simhash

class comsimhash(NFPlugin):

    #识别端口号，来确定对应的服务情况
    def judge_port(self, packet, flow):
        if (flow.dst_port == 80 or flow.dst_port == 443):
            flow.udps.label = 'web'
        elif (flow.dst_port == 21):
            flow.udps.label = 'ftp'
        elif (flow.dst_port == 23):
            flow.udps.label = 'telnet'
        elif (flow.dst_port == 25):
            flow.udps.label = 'smtp'
        elif (flow.dst_port == 3306):
            flow.udps.label = 'mysql'
        elif (flow.dst_port == 22):
            flow.udps.label = 'ssh'
        elif (flow.dst_port == 110):
            flow.udps.label = 'pop3'
        elif (flow.dst_port == 53):
            flow.udps.label = 'dns'

        if (flow.udps.label == ''):
            flow.udps.label = flow.application_category_name

    #根据持续时间，request_server_name的信息，来判断是否是视频流
    def judge_video(self, packet, flow):
        video_name = ['youku','tudou','aiqiyi','qq']   #后续补充视频网站地址
        if (packet.dst_port == '443' or packet.dst_port == '80'):
            if (packet.src2dst_bytes >= 1000 and packet.requested_server_name in video_name): #判断流传递的数据是否超过10秒，如果是，则可能是视频流
                result = [v for v in video_name if packet.requested_server_name in video_name]  #提取匹配的字符串名称
                flow.udps.label = result

    #接着判断加密流量, 加密流量则计算目的ip地址，目的mac地址，目的服务器request请求，构成一个加密流量
    def judge_encrypt(self, packet, flow):
        encrypinfo = str(flow.src_port + flow.dst_port + flow.protocol + flow.dst2src_packets) #后续再调整补充
        flowsimhashvalue = Simhash(encrypinfo)
        flow.udps.flowsimhashvalue = flowsimhashvalue

        return flowsimhashvalue

    def on_init(self, packet, flow):
        flow.udps.label = ''
        self.on_update(packet, flow)

    def on_update(self, packet, flow):

        # 首先提取源端口等相关信息的hash值存下来，然后得到对应的simhash值，暂时还没写
        self.judge_encrypt(packet, flow)

        # 首先通过持续时间和请求内容，来判断是否是视频流
        self.judge_video(packet, flow)

        if(flow.udps.label == ''):
            #判断端口号
            self.judge_port(packet, flow)


def main():
    #i = 0
    my_awesome_streamer = NFStreamer(source="youku.pcap",statistical_analysis=False,n_dissections=255,udps=comsimhash(accouncting_mode=1))  # or network interface (source="eth0")
    my_dataframe = my_awesome_streamer.to_pandas(columns_to_anonymize=[])
    #输出到csv文件
    my_awesome_streamer.to_csv(path=None, columns_to_anonymize=[], flows_per_file=0, rotate_files=0)

if __name__ == "__main__":
    main()

