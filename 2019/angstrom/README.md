

# angstrom CTF

## Abstract

- Weight of CTF time : 22.98
- Format : Jeopardy
- Difficulty : :star:
- Novelty : :star:



## Overview

### Pwnable

- **over my brain** : `brain fuck`을 활용한 SBOF
- **server** : 출제자가 어셈블리단위로 작업했기 때문에, 어셈단위로 보지 않으면 풀기 어렵다. 취약점이 굉장히 억지스럽다.
- **weeb hunting **: UAF와 double-free bug로 푸는 문제. 정말 쓸데 없는 rand()함수의 남발로 시간이 오래걸리고, 익스를 짜기가 귀찮다. 좋은 문제는 아니다. :thumbsdown:





---

## Challenge List

|        Name         | Category |     Difficulty     |      Worth       |   Write up   |         Tags         |
| :-----------------: | :------: | :----------------: | :--------------: | :----------: | :------------------: |
|      aquarium       |   pwn    |       :star:       |     :dollar:     | :black_flag: |        `SBOF`        |
|    chain of rope    |   pwn    |       :star:       |     :dollar:     | :black_flag: |        `ROP`         |
|    over my brain    |   pwn    |       :star:       |     :dollar:     | :black_flag: | `brain fuck`, `SBOF` |
|      pie shop       |   pwn    |       :star:       |     :dollar:     | :black_flag: |    `pie`,`brute`     |
|      purchases      |   pwn    |       :star:       |     :dollar:     | :black_flag: |        `fsb`         |
|       returns       |   pwn    |       :star:       |     :dollar:     | :black_flag: |        `fsb`         |
|       server        |   pwn    |    :star::star:    |     :dollar:     | :black_flag: |        `asm`         |
|    weeb hunting     |   pwn    |    :star::star:    |     :dollar:     |      -       |        `dfb`         |
|       bugger        |   rev    | :star::star::star: | :dollar::dollar: |      -       |     `anti-debug`     |
| high quality checks |   rev    |       :star:       |     :dollar:     |      -       |        `angr`        |
|      I like it      |   rev    |       :star:       |     :dollar:     | :black_flag: |        `noob`        |
|       icthyo        |   rev    |    :star::star:    |     :dollar:     |      -       |        `png`         |
|    intro to rev     |   rev    |       :star:       |     :dollar:     | :black_flag: |        `noob`        |
|      one bite       |   rev    |       :star:       |     :dollar:     | :black_flag: |        `noob`        |
