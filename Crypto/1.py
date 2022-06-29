
import string
import hashlib

strs = string.ascii_lowercase + string.ascii_uppercase + '0123456789'
pa = 'd9ddd1800f'
for i in strs:
    for j in strs:
        for k in strs:
            for l in strs:
                s = i + j + k +l
                m = hashlib.md5()
                m.update(s.encode('utf-8'))
                st = m.hexdigest()
                if (pa in st):
                   print(st)