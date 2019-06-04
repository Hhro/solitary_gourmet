s2l = lambda s : [ord(x) for x in s]
l2s = lambda l : ''.join([chr(x) for x in l])

v2=s2l('5B4D614A505B485F5645584A5D4D563E'.decode('hex')[::-1])
v4=s2l('615F615057614D49515A50574961505B'.decode('hex')[::-1])
v3=v2[0]
rest=[0x49,0x56,0x57,0x52,0x5b,0x43]


res=[]

for x in v2:
	res.append(x^v3)

for x in v4:
	res.append(x^v3)

for x in rest:
	res.append(x^v3)

print l2s(res)[1:]