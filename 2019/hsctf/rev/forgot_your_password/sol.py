import random
ch = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ '

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
def chr2bin(data):
    result = 0
    for c in data[::-1]:
    	result <<= 8
    	result += ord(c)
    return result


print hex(chr2bin('hsctfiss'))

x+y=0x7373696674637368
z = x^y
x` = ((x<<55)|(x>>9))^(z^(z<<14))
y` = (z<<36)|(z>>28)
x`+y`=0x776f776c6f6f636f

z = (y`<<28)|(y`>>36) = x^y
z = x`^((x<<55)|(x>>9))^(x<<14)^(y<<14)

x`^((x<<55)|(x>>9)) = (z^(z<<14))


print hex(chr2bin('ocoolwow'))