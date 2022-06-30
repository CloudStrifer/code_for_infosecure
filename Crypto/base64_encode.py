import base64

strs = bytes('1234dasjkjweajkwj23DJKJS8','utf-8')
print(strs)
strss = base64.b64encode(strs)

print(strss)