from PIL import Image
import numpy as np
import csv
import os
import pandas as pd

path = 'E:/PyCharmCode/Flow_extract/ITCF/csv/'

#循环读取csv文件
for filename in os.listdir(path):
    if filename.endswith('.csv'):
        sampled_data = pd.read_csv(path + filename, header=None)  #因为头部没有，所以不需要把头部当做列名
        sampled_data = pd.DataFrame(sampled_data)
        df_total = sampled_data.drop(sampled_data.columns[-1], axis=1)  # 把最右边那列去掉
        df_total = np.array(df_total)
        #文件保存路径
        savepath = 'E:/PyCharmCode/Flow_extract/FFEM/piciutre/' + filename[:-4] + '/'
        #判断文件夹是否已经创建，没有则创建
        if not os.path.exists(savepath):
            os.mkdir(savepath)

        i = 1
        #循环读取每一行数据，并保存为一张图片
        for row in df_total:
            tmp = row.reshape(32, 32)
            #图片尺寸的宽和高
            width, height = 32, 32
            #之前没有加这一行，所以一直导致创建的图像有很多数据丢失，现在没问题了
            tmp = tmp.astype(np.uint8)
            img = Image.fromarray(tmp, mode='L')
            # im = np.asarray(img)
            # img.show()
            if (i == 1000):
                break
            img.save(savepath + str(i) + '.png')
            i += 1
            #print(i)
        print("1")

