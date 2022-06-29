import gmpy2
# RSA
# N = p * q
# q 大素数
# p 大素数
# d 私钥
# e 公钥 65537
# m 明文
# c  密文
# c 密文  c=pow(m,e,N) 也就是c = m^e mod N
# m 明文 = pow(c,d,N)   也就是 m =  c^d mod N
# Phi = (p-1) * (q-1)
# d = invert (e,phi)

# dp=d%(p-1)
# dq=d%(q-1)

# c≡me(mod n) ①
# m≡cd(mod n) ②
# dp≡d(mod (p-1)) ③
# dq≡d(mod (q-1)) ④
# m = (((mp-mq)*I)%p)*q+mq       #求明文公式
# 其中：
# I = gmpy2.invert(q,p)
# mp = pow(c,dp,p)
# mq = pow(c,dq,q)

# 在一次RSA密钥对生成中，假设p=473398607161，q=4511491，e=17
# 求解出d作为flga提交
p = 473398607161
q = 4511491
e = 17
phi = (p-1) * (q-1)
d = gmpy2.invert(p,q)
print(d)