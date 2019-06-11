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

- **kpets**

- **rusty_shop**

- **asciishop**

- **raddest_db** 

  

### Reversing

- **imageprot**: 워밍업

------

## Challenge List

|         Name         | Category |        Difficulty        |          Worth           |   Write up   |            Tags            |
| :------------------: | :------: | :----------------------: | :----------------------: | :----------: | :------------------------: |
|      overfloat       |   pwn    |          :star:          |         :dollar:         | :black_flag: |             `one-byte overwrite`             |
|      otp_server      |   pwn    |          :star:          |         :dollar:         | :black_flag: |             `OOB`             |
|         rank         |   pwn    |          :star:          |         :dollar:         | :black_flag: |             `OOB`             |
|       babylist       |   pwn    |       :star::star:       |     :dollar::dollar:     |   :black_flag:    | `DFB`, `vector` |
|        kpets         |   pwn    |       X       |         X         | X | `kmod` |
|      rusty_shop      |   pwn    | X | X |      X       |         X          |
|      asciishop       |   pwn    |   X|         X         | X |      X       |
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

