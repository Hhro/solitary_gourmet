## Facebook CTF 2019

- Weight of CTF time : 24.62
- Format : Jeopardy
- Difficulty : :star::star::star:
- Novelty : :star::star::star: 
- Link : <https://www.fbctf.com/challenges>

## Overview

### **pwnable**

- **otp_server**: `snprintf`  + `one-byte overwrite`

- **rank**: 쉬운 OOB

- **babylist**: 전형적인 2.27 Double free + CPP 벡터 구조체의 할당과 해제

- **kpets**: 코드가 굉장히 이상하게 짜여져 있어서 더 이해하기가 어렵다. 커널 레벨 레이스컨디션.

- **rusty_shop**: 러스트는 demangle을 해도 분석하기가 참 난해하다. 좀 더 깔쌈하게 리버싱하는 방법이 없을까. oneday 취약점을 찾아서 공략하는게 재밌는 문제. Vtable이 덮여서 풀리는건 알겠는데, 정확히 어떻게 트리거가 되는건지는;;

- **asciishop**

- **raddest_db** 

  

### Reversing

- **imageprot**: 워밍업

------

## Challenge List

|         Name         | Category |        Difficulty        |          Worth           |   Write up   |            Tags            |
| :------------------: | :------: | :----------------------: | :----------------------: | :----------: | :------------------------: |
|      [overfloat](pwn/overfloat)      |   pwn    |          :star:          |         :dollar:         | :black_flag: |             `one-byte overwrite`             |
|      [otp_server](pwn/otp_server)      |   pwn    |          :star:          |         :dollar:         | :black_flag: |             `OOB`             |
|         [rank](pwn/rank)         |   pwn    |          :star:          |         :dollar:         | :black_flag: |             `OOB`             |
|       [babylist](pwn/babylist)       |   pwn    |       :star::star:       |     :dollar::dollar:     |   :black_flag:    | `DFB`, `vector` |
|     [kpets](pwn/kpets)     |   pwn    |       :star::star:       |         :dollar::dollar::dollar:         | :flags: | `kmod`,`race_condition` |
|      [rusty_shop](pwn/rusty_shop)      |   pwn    | :star::star::star: | :dollar::dollar::dollar: |      :triangular_flag_on_post:      |         `rust`,`CVE`,`integer_overflow`         |
|      [asciishop](pwn/asciishop/)      |   pwn    | :star::star::star: |         :dollar::dollar::dollar:         | :flags: |      X       |
|      raddest_db      |   pwn    |            X             |         X         |      X       |        X         |
|      imageprot       |   rev    |            :star:             |         :dollar:         | :black_flag: |          -          |
| SOMBRERO ROJO(part1) |   rev    |            X             |         X         | X |             X              |
|   go_get_the_flag    |   rev    |            X             |            X             |      X       |             X              |
|      matryoshka      |   rev    |      X       |        X         |      X       |    X    |
| SOMBRERO ROJO(part2) |   rev    |      X       |        X         |      X      |       X       |
|   nomoreeasycrypt    |   rev    |      X       |        X         |      X      |     X     |
|   products manager   |   web    |      X       |        X         |      X      |     X     |
|        pdfme         |   web    |      X       |        X         |      X      |        X        |
|  secret note keeper  |   web    | X | X | X | X |
|      rceservice      |   web    | X | X | X | X |
|        events        |   web    | X | X | X | X |
|   hr_admin_module    |   web    | X | X | X | X |

