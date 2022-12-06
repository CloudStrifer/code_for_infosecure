import requests



for i in range(1,2):
    url = "http://10.1.10.10/event/25/awd/flag/?token=24a0fb3179dc8e56&flag="
    flag = 'flag{88e7e3ecb23cbadc812a50d048bbb591}'
    url = url + flag
    # passwd="password"
    # payload = {
    #     passwd: 'system("cat flag.txt");'
    # }
    res=requests.post(url)
    print(res.text)