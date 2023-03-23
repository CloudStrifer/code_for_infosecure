import pandas as pd
from sklearn.preprocessing import StandardScaler

#文件路径
csv_path = 'youku.new.csv'

#标准化单位。需要统一标准的有不少，首先是时间，除以1000,得到单位为s
#其次是bytes字节数，除以1024，得到单位是Kb
def standard_unit(df):
    df['bidirectional_duration_ms'] = df['bidirectional_duration_ms'] / 1000   #之前该时间的单位是毫秒
    df['dst2src_duration_ms'] = df['dst2src_duration_ms'] / 1000
    df['src2dst_duration_ms'] = df['src2dst_duration_ms'] / 1000

    df['bidirectional_bytes'] = df['bidirectional_bytes'] / 1024   #之前该单位是位
    df['src2dst_bytes'] = df['src2dst_bytes'] / 1024
    df['dst2src_bytes'] = df['dst2src_bytes'] / 1024

    return df

if __name__ == '__main__':
    df = pd.read_csv(csv_path)
    df = standard_unit(df)
    x_train, y_train = df.drop(columns=['label']),df['label']

    # 既然不做机器学习，那么就可以把这个模型规范化关闭掉
    # scaler = StandardScaler()
    # scaler = scaler.fit(x_train)
    # x_train = scaler.transform(x_train)
    print(x_train)


