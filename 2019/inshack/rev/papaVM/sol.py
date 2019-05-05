def calc(insp):
	mem=[0 for i in range(244*4)]
	mem[0]=31

	for i in range(4,244*4,4):
		mem[i]=(mem[i-4]*31)&0xffffffff

	lines=[0x01020000,0x01030000,0x01070400,0x01080100,0x02030600,
	0x03090000,0x04040000,0x04050100,0x08040500,0x05020400,0x05000700,
	0x05010800,0x05030800,0x06f70000,0x07020000]
	flag=0

	n=0xFFFFFFC8B0EB3225
	buf=[0,0,0,0,0,0,len(insp),0,0]

	byte1=lambda x: (x>>8)&0xff
	byte2=lambda x: (x>>16)&0xff
	hibyte=lambda x: (x>>24)&0xff

	res=0
	i=0
	while 1:
		line=lines[i]
		cmd=hibyte(line)
		arg1=byte1(line)
		arg2=byte2(line)
		if cmd==1:
			buf[arg2]=arg1
			i+=1
		if cmd==2:
			flag=(buf[arg2]==buf[arg1])
			if buf[3] > 45:
				print 'E'
				quit()
			i+=1
		if cmd==3:
			if flag:
				i+=(arg2)
			else:
				i+=1
		if cmd==4:
			buf[arg2]=0
			if arg2==5:
				buf[5]=insp[buf[1]]
				i+=1
			else:
				buf[arg2]=mem[buf[0]]
				i+=1
		if cmd==5:
			if buf[arg1] >= 0x8000000000000000:
				buf[arg1] = -(0x10000000000000000-buf[arg1])
			buf[arg2]+=buf[arg1]
			i+=1
		if cmd==6:
			i-=9
		if cmd==7:
			res=buf[(line>>16)&0xf]
			i+=1
			break
		if cmd==8:
			if buf[arg2] >= 0x80000000:
				buf[arg2] = -(0x100000000-buf[arg2])
			buf[arg2] *= buf[arg1]
			if buf[arg2] < 0:
				buf[arg2] = 0x10000000000000000+buf[arg2]
			i+=1

	if res<0:
		res=0x10000000000000000+res

	return res

def find_candid():
    n=0xFFFFFFC8B0EB3225
    for k in range(0x2f,0x7f):
            x=[k for _ in range(45)]
            x[44]=10
            for i in range(45):
                    for j in range(0x2f,0x7f):
                            x[i]=j
                            res=calc(x)
                            if abs(res-n) <= 0x10000000 and abs(n-res)%31==0:
                                return x,(n-res)

n=0xFFFFFFC8B0EB3225
candid,diff=find_candid()
print "candid: ",candid
print "diff: "+str(diff)
if diff<0:
    diff *= -1
    mf = 1

diff/=31
res=[]
while diff!=0:
    res.append(diff%31)
    diff/=31

if len(res)>=6:
    print "This candid is improper"
    print "try again"
    quit()
else:
    print "adjusting..."
    for i in range(len(res)):
        if mf:
            candid[i]-=res[i]
        else:
            candid[i]+=res[i]

print 'pass is:'+ ''.join(chr(x) for x in candid)
