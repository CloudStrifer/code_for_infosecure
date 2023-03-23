import csv
import pandas as pd

#文件路径
csv_path = 'youku.pcap.csv'
#导出文件命名
new_csv_name = 'youku.new.csv'

# 对每一列的类别数据进行判断，猜测是否是Unspecified，如果是，则对其进行修改
def adjust_label(label,application_category_name):

    if(label == 'Unspecified' and application_category_name != 'Unspecified'):
        label = application_category_name
    return label

#统一调整名称为小写
def adjust_format(label):
    label = str(label).lower()
    return label

# 删除多余特征
def del_redundant_feature(df):
    df = df.drop(['id','expiration_id','src_ip','src_mac','src_oui','dst_ip','dst_mac','dst_oui','vlan_id',
                  'tunnel_id','bidirectional_first_seen_ms','bidirectional_last_seen_ms','src2dst_first_seen_ms',
                  'src2dst_last_seen_ms','dst2src_first_seen_ms','dst2src_last_seen_ms','application_name',
                  'application_is_guessed','application_confidence','requested_server_name','client_fingerprint'
                  ,'server_fingerprint','user_agent','content_type','application_category_name'], axis=1)  # 删除多余的列
    return df

# 计算双向数据比
def add_new_feature(df):
    df["src2dst_bytes_data_ratio"] = df['src2dst_bytes'] / df['bidirectional_bytes']
    df["dst2src_bytes_data_ratio"] = df['dst2src_bytes'] / df['bidirectional_bytes']
    return df

if __name__ == '__main__':
    df = pd.read_csv(csv_path)
    # 修改列, 在执行该步骤前，必须将列udps.label的名称改为label，因为貌似不支持带有小数点的内容^_^.
    # flowsimhashvalue也改了。。
    df.rename(columns={'udps.label':'label'},inplace=True)
    df.rename(columns={'udps.flowsimhashvalue':'flowsimhashvalue'},inplace=True)

    df.label = df.apply(lambda x: adjust_label(x.label,x.application_category_name), axis=1)
    df.label = df.apply(lambda x: adjust_format(x.label), axis=1)

    df = del_redundant_feature(df)
    df = add_new_feature(df)

    #输出处理好的文件
    df.to_csv(new_csv_name)

    print(df['label'].value_counts())
