# TG:HACK

## Abstract

- Weight of CTF time : 0.00
- Format : Jeopardy
- Difficulty : :star::star:
- Novelty : :star: 
- Link : <https://tghack.no/> (avail until 2020)

CTF for noobs and intermediate.



## Overview

### **pwnable**

*전반적으로 평이. V8빼고*

- **pwntion 1,2,3**: 정말 정말 쉽다. 이제막 포너블 공부를 시작한 사람한테 적합함. 

- **The great bank heist**: `KVM`을 기반으로 했지만, 익스플로잇이 아주 쉽기 때문에, `kvm`에 대해 전혀 몰랐다면 `kvm`공부를 할 겸 풀어보면 좋을 듯 싶다.

- **Are you flipping kidding me?**: 간단한 bitflip 문제로, 대놓고 취약한 바이너리지만 제한사항이 있어서 이리저리 `GOT overwrite`를 하기위해 고민을 좀 해야한다. 푸는건 귀찮지만 새로 알게될 건 없다.

- **Baby's first javascript exploitation**: 최근 CTF 트렌드(?)인 Google의 V8엔진을 소재로한 문제. 공식 git에 올라온 소스를 일부러 취약하게 수정하고 빌드한 것이 문제로 주어진다. 출제자는 35c3의 Krautflare을 기반으로 난도를 낮춰서 출제했다고 하지만 V8을 모르는 사람에게는 그러나저러나 어렵다. V8에 관심이 있다면 V8을 공부하면서 풀어보면 좋다.

  

### Reversing

*리버싱을 좀 해봤다면 굳이 풀 필요는 없음*

- **Gotta Catch' Em All**: 직접 컨택이 필요한 문제인 것 같아서 손대지 않았다.



### Web

*다양한 테마를 갖췄지만, 난이도는 낮음*



---

## Challenge List

|                 Name                 | Category |     Difficulty     |      Worth       |   Write up   |            Tags            |
| :----------------------------------: | :------: | :----------------: | :--------------: | :----------: | :------------------------: |
|               pwntion1               |   pwn    |       :star:       |     :dollar:     | :black_flag: |             -              |
|               pwntion2               |   pwn    |       :star:       |     :dollar:     | :black_flag: |             -              |
|               pwntion3               |   pwn    |       :star:       |     :dollar:     | :black_flag: |             -              |
|         The great bank heist         |   pwn    |    :star::star:    | :dollar::dollar: |   :flags:    |  `KVM`, `16bit assembly`   |
|     Are You Flipping Kidding Me?     |   pwn    |    :star::star:    |     :dollar:     | :black_flag: | `bitflip`,`GOT overwrite ` |
| Baby's First JavaScript Exploitation |   pwn    | :star::star::star: | :dollar::dollar::dollar: |      X       |         `js`,`v8`          |
|              Bytecodes               |   rev    |       :star:       |     :dollar:     | :black_flag: |      `pyc decompile`       |
|   Gringotts Digitalization Project   |   rev    |       :star:       |     :dollar:     |      -       |        `proc file`         |
|            Cracking Magic            |   rev    |       :star:       |     :dollar:     | :black_flag: |          `brute`           |
|             Elfish flag              |   rev    |       :star:       |     :dollar:     | :black_flag: |             -              |
|         Gotta Catch 'Em All          |   rev    |         X          |        X         |      X       |             -              |
|            Fortune cookie            |   web    |       :star:       |     :dollar:     |      -       |    `cookie`, `guessing`    |
|               Imagicur               |   web    |       :star:       |     :dollar:     |      -       |       `file upload`        |
|               Wandshop               |   web    |       :star:       |     :dollar:     |      -       |     `request forgery`      |
|               itsmagic               |   web    |       :star:       |     :dollar:     |      -       |     `IDOR`,`guessing`      |
|             Wizardschat              |   web    |    :star::star:    |     :dollar:     |      X       |        `flask SSTI`        |

