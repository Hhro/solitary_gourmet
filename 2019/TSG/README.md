# TSG CTF

## Abstract

- Weight of CTF time : 0.00
- Format : Jeopardy
- Difficulty : ​TBU​
- Novelty : TBU
- CTF time : <https://ctftime.org/event/758>



## Overview

### **pwnable**

- Super Smash Bros : pseudo file system을 공격하는 문제. 이용하는 취약점은 사소하지만, 공격 과정이 흥미롭다.

- Odd Multiplier : 간단한 오버플로우를 통해 `return`주소를 덮는 기본적인 스택 버퍼오버플로우 문제. Partial overflow를 통해 값을 덮는데, 이 과정이 흥미로움.

  



---

## Challenge List

|                 Name                 | Category |     Difficulty     |      Worth       |   Write up   |            Tags            |            Solves            |
| :----------------------------------: | :------: | :----------------: | :--------------: | :----------: | :------------------------: | :----------------------------------: |
|     Super Smash Bros     |   pwn    |       :star::star:       |     :dollar::dollar:     | :black_flag: |             `fs`,`tcache`,`dfb`             |             11             |
|               Odd Multiplier               |   pwn    | :star::star: | :dollar::dollar: | :black_flag: |             `partial overwrite`, `sbof`             |             10             |
|               Capacity Oriented Vector               |   pwn    |      X       |    X     |      X       |             X              |             6             |
|         STLC         |   pwn   |      X       |    X     |      X       |          X          |          0          |
|           ffi            |   rev   |      X       |    X     |      X       |          X          |          19          |
| ESO VM | rev | X | X | X | X | 2 |
|      BADNONCE Part1      |   web   |      X       |    X     |      X       |          X          |          15          |
|              BADNONCE Part2              |   web   |      X       |    X     |      X       |          X          |          8          |
|       Secure Bank        |   web   |      X       |    X     |      X       |          X          |          10          |
|          RECON           |   web   |      X       |    X     |      X       |          X          |          3          |

