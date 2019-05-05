# INS'hAck 2019

## Abstract

- Weight of CTF time : 29.65

- Format : Jeopardy

- Difficulty : :star::star:

- Novelty : :star::star:

- CTF time link: <https://ctftime.org/event/763>

  

## Overview

### **pwnable**

*전반적으로 쉬움*

- **integerover, signed or not signed, ropberry, gimme your shell** : warm up

- **OverCobol** : 코볼로 작성된 프로그램을 익스플로잇하는 나름 특이한 문제. 풀면서 코볼 공부가 좀 된다.

- **hell of a jail**:  잊을만하면 나오는 python3기반 pyjail 문제로, pyjail 하면 떠오르는 것들이 다 들어있다. 이거 하나 풀어보면 왠만한 pyjail문제는 다 풀 수 있다.

- **john cena**: 바이너리가 주어지지 않는 블라인드 포맷스트링 문제. 이런 유형의 문제는 한 번 정도만 풀어보면 다음에 블라인드 문제를 만났을 때 도움이 될 것 같다.

  

### Reversing

- **PaPaVM**: trivial한 껍질 벗기기? 과정을 거치면, 최종 바이너리로 VM이 등장한다. VM을 이해하기는 쉬우나, 풀이를 떠올리기는 좀 난해하다.



---

## Challenge List

|                 Name                 | Category |     Difficulty     |      Worth       |   Write up   |            Tags            |
| :----------------------------------: | :------: | :----------------: | :--------------: | :----------: | :------------------------: |
|               integerover               |   pwn    |       :star:       |     :dollar:     | :black_flag: |             `int overflow`             |
|               signed or not signed               |   pwn    |       :star:       |     :dollar:     | :black_flag: |             `type casting`             |
|       OverCobol        |   pwn    |       :star:       |     :dollar::dollar:     | :flags: |             `cobol`,`bof`             |
|    gimme-your-shell    |   pwn    |    :star:    | :dollar: | :black_flag: |   `shell coding`   |
|        ropberry        |   pwn    |    :star:    |     :dollar:     | :black_flag: |       `ROP`        |
|     hell_of_a_jail     |   pwn    | :star::star: | :dollar::dollar: |      :flags:      | `python3`,`pyjail` |
|       john-cena        |   pwn   |       :star::star:       |     :dollar::dollar:     |   :flags:    |   `fsb`,`blind`    |
|   Dashlame - Part 1    |   rev    |       :star:       |     :dollar:     |      -       |       `pyc`        |
|  Obscure File Format   |   rev    |      X       |        X         |      X       |         X          |
|             xHell             |   rev    |      X       |        X         |      X       |             X              |
|         Deaddrop Filesystem         |   rev    |         X          |        X        |      X       |             X              |
|     useless-chall      |   rev   |      X       |        X         |      X       |         X          |
|               PaPaVM               |   rev   |       :star::star:       |     :dollar:     | :black_flag: |    `VM`,`brute`    |
|               Exploring The Universe               |   web    |       :star:       |     :dollar:     |      -       |  `dir traversal`   |
|         atchap         |   web    |      X       |        X         |      x       |         X          |
|       unchained        |   web    |      X       |        X         |      X       |         X          |
|  bypasses-everywhere   | web | X | X | X | X |
| bypasses-everywhere v2 | web | X | X | X | X |

