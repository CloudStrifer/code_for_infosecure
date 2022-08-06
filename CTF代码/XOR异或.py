import base64
# 必须使用python2版本，python3版本则运行不了
#  Xor??
# 结果flag{2F64B7656E77E0A0743C02ECAE9E2513}
a = 'AAoHAR1UIFBSJFFQU1AjUVEjVidWUVJVJVZUIyUnI18jVFNXVRs='
a = base64.b64decode(a)

for i in range(128):
    s = ''
    for j in a :
        s = s + chr(i^ord(j))
    if 'flag' in s:
        print(s)








