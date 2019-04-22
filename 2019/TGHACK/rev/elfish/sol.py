x='C8D2C9CDD6CAC3D8D7C9C6C3D7DDCBCBC5D0CADF9D95ABB8'
x=x.decode('hex')
x=[chr(ord(p)-100) for p in x]
print ''.join(x[::-1])


