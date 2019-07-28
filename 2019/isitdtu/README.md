# ISITDTU CTF 2019 Quals

## Abstract📁

- Weight of CTF time : 0.00
- Format : Jeopardy
- Difficulty : :star::star:
- Novelty : :star: 
- Link : https://ctf.isitdtu.com/



## Overview

### **pwnable**

*전반적으로 평이*

- iz_heap_lv1 : OOB

- iz_heap_lv2 : null byte overflow

- babyshellcode : alarm을 이용한 time based info leak.

  

### Reversing

*상태가 별로;*

- Recovery : 중위, 후위로 표현된 트리를 전위트리로 변환
- Pytecode : python bytecode를 disassemble해서 주는데, 처음 보는 형태의 문제였으나 귀찮기만 하다.
- Re01 : Super guessing problem. 이렇게 솔브가 적게나올 문제가 아닌데 게싱이 좀 심하다.



### Web

- Rose Garden : Warm up



------

## Challenge List

|     Name      | Category | Difficulty |      Worth       |   Write up   |         Tags         |
| :-----------: | :------: | :--------: | :--------------: | :----------: | :------------------: |
|  iz_heap_lv1  |   pwn    |   :star:   |     :dollar:     | :black_flag: |        `oob`         |
|  iz_heap_lv2  |   pwn    |   :star:   |     :dollar:     | :black_flag: | `null-byte overflow` |
| babyshellcode |   pwn    |   :star:   | :dollar::dollar: | :black_flag: |  `time based leak`   |
|   Tokenizer   |   pwn    |     x      |        x         |      x       |          `x          |
|  prisonbreak  |   pwn    |     x      |        x         |      x       |          `x          |
|   Recovery    |   rev    |   :star:   |     :dollar:     |      -       |  `jar`, `algorithm`  |
|   Pytecode    |   rev    |   :star:   |     :dollar:     |      -       |       `python`       |
|     Re01      |   rev    |   :star:   |        NO        |      -       |          -           |
|    CHIACAX    |   rev    |     x      |        x         |      x       |          x           |
|     3006      |   rev    |     x      |        x         |      x       |          x           |
|    GoFast     |   rev    |     x-     |        -x        |      x-      |          x           |
|   Crack me    |   rev    |     x      |        x         |      x       |          x           |
|  Rose Garden  |   web    |   :star:   |     :dollar:     |      -       |          -           |
|   XSSgame1    |   web    |     x      |        x         |      x       |          x           |
|    EasyPHP    |   web    |     x      |        x         |      x-      |          `x          |
|   XSSgame2    |   web    |     x      |        x         |      x       |          x           |

