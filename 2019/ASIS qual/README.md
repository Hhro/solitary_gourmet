# ASIS qual

## Abstract

- Weight of CTF time : 61.74
- Format : Jeopardy
- Difficulty : :star::star:
- Novelty : :dollar:



## Overview

### Pwnable

- **Silk roadI** : 익스플로잇 내용은 간단하지만, 좀 귀찮다.

- **precise Average** : 쉽다.

- **pwn101** : `tcache`와 힙 `one byte overflow`가 섞인 문제. `tcache` 연습문제 정도로 괜찮을 듯.

- **BabyVM1** : 디스어셈블러 짜는게 상당히 귀찮다. 익스플로잇은 수월한편

  

### Reversing

- **keymaker** : 선형대수학😬

- **Medias** : 분석은 전체적으로 쉬움. 최종적으로 확인된 조건식을 `z3`로 푸는게 핵심인 문제. `z3`를 공부할겸 풀면 좋다.

  

---

## Challenge List

|      Name       | Category |  Difficulty  |      Worth       |   Write up   |             Tags             |
| :-------------: | :------: | :----------: | :--------------: | :----------: | :--------------------------: |
|   Silk roadI    |   pwn    | :star: |     :dollar:     | :black_flag: |   `SBOF`,`ROP`,`leave-ret`   |
|   Silk roadII   |   pwn    |      X       |        X         |      X       |              X               |
|  Silk roadIII   |   pwn    |      X       |        X         |      X       |              X               |
| precise Average |   pwn    | :star: |     :dollar:     | :black_flag: |   `SBOF`,`ROP`,`leave-ret`   |
|  Double cream   |   pwn    |      X       |        X         |      X       |            `fsb`             |
|     pwn101      |   pwn    | :star::star: |     :dollar::dollar:     | :black_flag: | `tcache`,`one byte overflow` |
|     BabyVM1     |   pwn    | :star::star::star: | :dollar::dollar: | :flags: |              `vm`              |
|    Keymaker     |   rev    | :star::star: | :dollar::dollar: | :black_flag: |       `linear algebra`       |
|     Medias      |   rev    |      :star: | :dollar::dollar: |      :flags:      |              `z3`              |
|   Archimedes    |   rev    |      X       |        X         |      X       |              X               |
|    Mindspace    |   rev    |      X       |        X         |      X       |              X               |
|    Seatbelt     |   rev    |      X       |        X         |      X       |              X               |
|      Xarch      |   rev    |      X       |        X         |      X       |              X               |
