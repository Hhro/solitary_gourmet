def u16(s):
    return ord(s[0]) + (ord(s[1])<<8)

def u32(s):
    res = 0
    for i in range(4):
        res += ord(s[i]) << (i*8)
    return res

def argp1(arg_byte):
    return arg_byte&0xf, arg_byte>>4

def expand_stack(arg): #1
    global res
    global idx
    global sp
    res += "{}. sub sp, {}\n".format(idx,hex(ord(arg)))
    sp -= ord(arg)
    idx += 2

def mov_rr_byte(arg1,arg2): #2
    global res
    global idx
    res += "{}. mov $reg{}, $reg{}\n".format(idx,arg1,arg2)
    idx += 2

def mov_rs_byte(arg1,arg2): #3
    global res
    global idx
    global sp
    res += "{}. mov $stack[{}+$reg{}], $reg{}\n".format(idx,hex(sp),arg1,arg2)
    idx += 2

def mov_mr_byte(arg1,arg2): #4
    global res
    global idx
    res += "{}. mov $reg{}, BYTE PTR data[$reg{}]\n".format(idx,arg1,arg2)
    idx += 2

def jif(arg1,arg2): #5
    global res
    global idx
    res += "{}. test $reg{}\n".format(idx,arg1)
    res += "{}jz {}\n\n".format(' '*len(str(idx)+'ab'),(arg2-0x4000))
    idx += 4

def ret(): #6
    global res
    global idx
    res += "{}. ret\n\n".format(idx)
    idx += 1

def mov_dr_dword(arg1,arg2): #7
    global res
    global idx
    res += "{}. mov $reg{}, data[$reg{}]\n".format(idx,arg1,arg2)
    idx += 2

def syscall_read_stack(arg1,arg2): #8
    global res
    global idx
    global sp
    res += "{}. read(0,stack[{}+$reg{}],$reg{})\n".format(idx,hex(sp),arg1,hex(arg2))
    idx += 2

def mov_rm_dword(arg1,arg2): #0xa
    global res
    global idx
    res += "{}. mov DWORD PTR data[$reg{}], $reg{}\n".format(idx,arg1,arg2)
    idx += 2

def put_chunk_byte(arg1,arg2,arg3): #0xd
    global res
    global idx
    res += "{}. BYTE PTR chunk[$reg{}][$reg{}+4] = BYTE PTR $reg{}\n".format(idx,arg1,arg2,arg3)
    idx += 3

def get_chunk_dword(arg1,arg2,arg3): #0xe
    global res
    global idx
    res += "{}. mov $reg{}, DWORD PTR chunk[$reg{}][$reg{}+1]\n".format(idx,arg1,arg2,arg3)
    idx += 3

def sub_rr(arg1,arg2): #0x12
    global res
    global idx
    res += "{}. sub $reg{}, $reg{}\n".format(idx,arg1,arg2)
    idx += 2

def put_chunk_dword(arg1,arg2,arg3): #0x13
    global res
    global idx
    res += "{}. DWORD PTR chunk[$reg{}][$reg{}+1] = DWORD PTR $reg{}\n".format(idx,arg1,arg2,arg3)
    idx += 3

def mov_sr_byte(arg1,arg2): #0x14
    global res
    global idx
    global sp
    res += "{}. mov $reg{}, stack[{}+$reg{}]\n".format(idx,arg1,hex(sp),arg2)
    idx += 2

def free_chunk(arg1): #0x15
    global res
    global idx
    res += "{}. call free(chunk[$reg{}])\n".format(idx,arg1)
    idx += 2

def free_stack(arg1): #0x16
    global res
    global idx
    global sp
    res += "{}. add sp, {}\n".format(idx,hex(arg1))
    sp += arg1
    idx += 2

def call(arg1): #0x18
    global res
    global idx
    res += "{}. call {}\n\n".format(idx,arg1-0x4000)
    idx += 3

def syscall_write_stack(arg1,arg2): #0x19
    global res
    global idx
    global sp
    res += "{}. write(1,stack[{}+$reg{}],{})\n".format(idx,hex(sp),arg1,hex(arg2))
    idx += 2

def jnz(arg1,arg2): #0x1b
    global res
    global idx
    res += "{}. test $reg{}\n".format(idx,arg1)
    res += "{}jnz {}\n\n".format(' '*len(str(idx)+'ab'),(arg2-0x4000))
    idx += 4

def get_chunk_byte(arg1,arg2,arg3): #0x1c
    global res
    global idx
    res += "{}. mov $reg{}, BYTE PTR chunk[$reg{}][$reg{}+4]\n".format(idx,arg1,arg2,arg3)
    idx += 3

def dead(arg1): #0x1f
    global res
    global idx
    res += "{}. exit({})\n".format(idx,arg1)
    idx += 2

def add_rr(arg1,arg2): #0x21
    global res
    global idx
    res += "{}. add $reg{}, $reg{}\n".format(idx,arg1,arg2)
    idx += 2

def malloc_dword(arg1): #0x24
    global res
    global idx
    res += "{}. call malloc(4*($reg{}+1))\n".format(idx,arg1)
    idx += 2

def jmp(arg1): #0x25
    global res
    global idx
    res += "{}. jmp {}\n".format(idx,arg1-0x4000)
    idx += 3

def malloc(arg1): #0x27
    global res
    global idx
    res += "{}. call malloc($reg{})\n".format(idx,arg1)
    idx += 2

def syscall_read(arg1,arg2): #0x28
    global res
    global idx
    res += "{}. read(0, data[$reg{}], $reg{})\n".format(idx,arg1,arg2)
    idx += 2

def syscall_write(arg1,arg2):
    global res
    global idx
    res += "{}. write(1, data[$reg{}], $reg{})\n".format(idx,arg1,arg2)
    idx += 2

def mov_cr_dword(arg1,arg2): #0x29
    global res
    global idx
    res += "{}. mov $reg{}, {}\n".format(idx,arg1,hex(arg2))
    idx += 6

def get_chunk_size(arg1,arg2): #0x2a
    global res
    global idx
    res += "{}. mov $reg{}, DWORD PTR chunk[$reg{}]\n".format(idx,arg1,arg2)
    idx += 2

with open("baby_code","rb") as code_in:
    code = code_in.read()

idx = 0
res = ""
sp = 0x1000

while 1:
    opc = ord(code[idx])
    if opc == 1:
        arg1 = code[idx+1]
        expand_stack(arg1)
    elif opc == 2:
        arg1, arg2 = argp1(ord(code[idx+1]))
        mov_rr_byte(arg1,arg2)
    elif opc == 3:
        arg1, arg2 = argp1(ord(code[idx+1]))
        mov_rs_byte(arg1,arg2)
    elif opc == 4:
        arg1 = ord(code[idx+1]) & 0xf
        arg2 = ord(code[idx+1]) >> 4
        mov_mr_byte(arg1,arg2)
    elif opc == 5:
        arg1 = ord(code[idx+1]) >> 4
        arg2 = u16(code[idx+2:idx+4])
        jif(arg1,arg2)
    elif opc == 6:
        ret()
    elif opc == 7:
        arg1, arg2 = argp1(ord(code[idx+1]))
        mov_dr_dword(arg1,arg2)
    elif opc == 8:
        arg1, arg2 = argp1(ord(code[idx+1]))
        syscall_read_stack(arg1,arg2)
    elif opc == 0xa:
        arg1, arg2 = argp1(ord(code[idx+1]))
        mov_rm_dword(arg1,arg2)
    elif opc == 0xb:
        arg1 = ord(code[idx+1])&0xf
        arg2 = ord(code[idx+1])>>4
        syscall_write(arg1,arg2)
    elif opc == 0xd:
        arg1,arg3 = argp1(ord(code[idx+1]))
        arg2 = ord(code[idx+2])>>4
        put_chunk_byte(arg1,arg2,arg3)
    elif opc == 0xe:
        arg1,arg2 = argp1(ord(code[idx+1]))
        arg3 = ord(code[idx+2])>>4
        get_chunk_dword(arg1,arg2,arg3)
    elif opc == 0x12:
        arg1, arg2 = argp1(ord(code[idx+1]))
        sub_rr(arg1,arg2)
    elif opc == 0x13:
        arg1, arg3 = argp1(ord(code[idx+1]))
        arg2 = ord(code[idx+2])>>4
        put_chunk_dword(arg1,arg2,arg3)
    elif opc == 0x14:
        arg1, arg2 = argp1(ord(code[idx+1]))
        mov_sr_byte(arg1,arg2)
    elif opc == 0x15:
        arg1 = ord(code[idx+1])>>4
        free_chunk(arg1)
    elif opc == 0x16:
        arg1 = ord(code[idx+1])
        free_stack(arg1)
    elif opc == 0x18:
        arg1 = u16(code[idx+1:idx+3])
        call(arg1)
    elif opc == 0x19:
        arg1, arg2 = argp1(ord(code[idx+1]))
        syscall_write_stack(arg1,arg2)
    elif opc == 0x1b:
        arg1 = ord(code[idx+1])>>4
        arg2 = u16(code[idx+2:idx+4])
        jnz(arg1,arg2)
    elif opc == 0x1c:
        arg1,arg2 = argp1(ord(code[idx+1]))
        arg3 = ord(code[idx+2])>>4
        get_chunk_dword(arg1,arg2,arg3)
    elif opc == 0x1f:
        arg1 = ord(code[idx+1])
        dead(arg1)
    elif opc == 0x21:
        arg1, arg2 = argp1(ord(code[idx+1]))
        add_rr(arg1,arg2)
    elif opc == 0x24:
        arg1 = ord(code[idx+1])>>4
        malloc_dword(arg1)
    elif opc == 0x25:
        arg1 = u16(code[idx+1:idx+3])
        jmp(arg1)
    elif opc == 0x27:
        arg1 = ord(code[idx+1])>>4
        malloc(arg1)
    elif opc == 0x28:
        arg1 = ord(code[idx+1])&0xf
        arg2 = ord(code[idx+1])>>4
        syscall_read(arg1,arg2)
    elif opc == 0x29:
        arg1 = ord(code[idx+1])&0xf
        arg2 = u32(code[idx+2:idx+6])
        mov_cr_dword(arg1,arg2)
    elif opc == 0x2a:
        arg1, arg2 = argp1(ord(code[idx+1]))
        get_chunk_size(arg1,arg2)
    else:
        error = "[error] opc {} is not defined.".format(hex(opc))
        break

with open("dis_code","w") as out:
    out.write(res)
