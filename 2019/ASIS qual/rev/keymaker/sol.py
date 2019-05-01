kp1=[0 for i in range(16)]
kp2=[0 for i in range(16)]
kp3=[0 for i in range(16)]
kp1[0:4]=[int(x,36) for x in 'ASIS']
c=[[0 for i in range(4)] for i in range(4)]

for i in range(4):
	for j in range(4):
		c[i][j] = 4*(i+j)

with open('dump.bin','rb') as f:
	dump = f.read()

dumps=[dump[0x40*i:0x40*(i+1)] for i in range(6)]

for i in range(6):
	dumps[i]=[int(dumps[i][4*j:4*j+4][::-1].encode('hex'),16) for j in range(16)]

for idx,dump in enumerate(dumps):
	p = [dump[4*i:4*i+4] for i in range(4)]
	dumps[idx]=p

for i in range(4):
	for j in range(4):
		for k in range(6):
			dumps[k][i][j]-=c[i][j]

for dump in dumps:
	for line in dump:
		print line
	print

keys=[10,28,18,28,0,7,17,3,22,4,7,27,1,33,33,33,29,27,1,23,18,7,34,10,23,13,23,14,24,0,24,0,20,3,34,22,4,20,3,27,24,27,4,12,21,14,3,0]

res=[]
for idx,key in enumerate(keys):
	if idx==16 or idx==32:
		res.append('_')
	if 0<=key and key<10:
		res.append(str(key))
	else:
		res.append(chr(key-10+ord('A')))

res[4]='{'
res[49]='}'

print ''.join(res)
