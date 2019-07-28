from z3 import *

intvec_to_int = lambda vec : Sum([vec[index] * (10**(len(vec)-index-1)) for index in range(len(vec))])
keys= []

for sz in range(1,10):
    s = Solver()

    part_size = sz
    key_size = part_size * 3

    key_vec = IntVector("key",key_size)
    key_val = Int("val")

    part1_val = Int("part1")
    part2_val = Int("part2")
    part3_val = Int("part3")

    for i in range(key_size):
        s.add(key_vec[i] >= 0)
        s.add(key_vec[i] < 10)
    
    s.add(key_val == intvec_to_int(key_vec))
    s.add(part1_val == intvec_to_int(key_vec[0:part_size]))
    s.add(part2_val == intvec_to_int(key_vec[part_size:2*part_size]))
    s.add(part3_val == intvec_to_int(key_vec[2*part_size:3*part_size]))

    #do median check
    for i in range(3):
        part_vec = key_vec[i*part_size : (i+1)*part_size]
        for j in range(1,part_size-1):
            s.add( part_vec[j-1] != 0)
            s.add( 2*part_vec[j] < part_vec[j-1] + part_vec[j+1])
    
    #do last weird check
    s.add(10**6 + part1_val <= 10**5 + part2_val)
    s.add(10**5 + part2_val <= 10**4 + part3_val)

    print "part_size = {}".format(sz)
    while s.check():
        try:
            m = s.model()
            keys.append(m[key_val].as_long())
            s.add(key_val > m[key_val].as_long())
        except:
            break

print "key : {}".format(keys[len(keys)-1])