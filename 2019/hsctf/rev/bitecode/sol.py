l2s = lambda l : ''.join([chr(x) for x in l])

x=[]

a=[189074585,189074673,-227215135,-227215214,19240864,19240899,245881291,245881279,
233391094,233390992,56978353,56978378,-213838484,-213838565,-231671677,-231671605,
-132473862,-132473910,143449065,143449053,108102484,108102411,71123188,71123073,
146096006,146096089,-173487738,-173487628,-116507045,-116507132,-68013365,-68013319,
171414622,171414529,94412444,94412524,
197453081,197453163,
-50622153,-50622201,
190140381,190140290,
77383944,77383996,
-41590082,-41590047,
61204303,61204283,
-24637751,-24637791,
61697107,61697122,
267894989,267895017,
-13480562,-13480461
]

'''
for i in range(len(a)):
	if a[i]<0:
		a[i]=0x100000000+a[i]
'''

for i in range(len(a)/2):
	x.append(a[2*i]^a[2*i+1])

print x

print l2s(x)