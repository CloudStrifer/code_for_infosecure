import pandas as pd


#文件路径
csv_finger = 'youku.new.csv'   #指纹库
csv_test = ''                 #测试数据


if __name__ == '__main__':
    df_finger = pd.read_csv(csv_finger)
    df_test = pd.read_csv(csv_test)

