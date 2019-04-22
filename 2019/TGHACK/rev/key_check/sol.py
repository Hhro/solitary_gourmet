import string
import random
from pwn import *

case = string.ascii_letters+string.digits

def func1(l):
    for i in range(0,12,2):
        if l[i]^l[i+1]^0x42>0x45:
            return 0
    return 1

def func2(l):
    for i in range(12,24,2):
        if l[i]^l[i+1]^19<=30:
            return 0
    return 1

serials=[]
cnt=0
while cnt<250:
    test = ''.join(random.sample(case,24))
    while test in serials:
        test = ''.join(random.sample(case,24))

    test=[ord(x) for x in test]
    if func1(test) and func2(test):
        cnt+=1
        print cnt
        serials.append(''.join([chr(x) for x in test]))
    
r=remote('keygen.tghack.no',2222)
for serial in serials:
    r.sendline(serial)

r.interactive()
