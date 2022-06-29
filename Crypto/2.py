# encoding: utf-8
import string
import hashlib
import requests

#payload = string.ascii_letters + string.digits + '_' #所有字母和数字
payload = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

requests.get()

for a in payload:
    for b in payload:
        for c in payload:
            for d in payload:
                strs = a + "ha" + b + "i" + c + "_go" + d + "d"
                ans = hashlib.sha1(strs).hexdigest()
                if ans.startswith('2aa90dc') == True:
                    print(strs)
                    exit(0)
