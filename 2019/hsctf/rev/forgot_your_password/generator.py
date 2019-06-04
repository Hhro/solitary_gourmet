#!/usr/bin/env python2

ch = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ '
s = [SECRET_1, SECRET_2]
# TOP SECRET: DO NOT LEAK
def lsh(x,k):
	return x<<k
def mask(a):
	return a&0xffffffffffffffff
def next():
	b = mask(s[0]+s[1])
	h()
	return mask(b)
def p(k, x):
	return x>>(64-k)
def xor(b, a):
	return a^b
def or_(a, b):
	return a|b
def h():
	s1 = mask(xor(s[0],s[1]))
	s[0] = mask(xor(or_(lsh(s[0],55),p(55,s[0])), xor(s1,(lsh(s1,14)))))
	s[1] = mask(or_(lsh(s1,36),p(36,s1)))

# Helper methods
def bin2chr(data):
    result = ''
    while data:
        char = data & 0xff
        result += chr(char)
        data >>= 8
    return result

def isp(d):
	if all(c in ch for c in d):
		return d
	else:
		return d.encode('hex')

# throw away first value for additional randomness
next()
next()

COMBO_NUM_1 = isp(bin2chr(next())) + isp(bin2chr(next()))
COMBO_NUM_2 = isp(bin2chr(next())) + isp(bin2chr(next()))
COMBO_NUM_3 = isp(bin2chr(next())) + isp(bin2chr(next()))   #'hsctfiss'+'ocoolwow'
print "Thanks! Your numbers are: "
print COMBO_NUM_1
print COMBO_NUM_2
print COMBO_NUM_3