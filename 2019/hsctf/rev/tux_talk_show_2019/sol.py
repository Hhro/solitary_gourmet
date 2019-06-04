from pwn import *
from ctypes import *
libc = CDLL("libc.so.6")
libc.srand(libc.time(0))

p=remote('rev.hsctf.com',6767)
#p=process('./trash')

base = 121+1231231+20312312+122342342+90988878+(-30)

for i in range(6):
    base -= libc.rand()%10 -1

p.sendline(str(base))
p.interactive()
