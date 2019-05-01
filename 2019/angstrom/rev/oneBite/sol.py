x=']_HZGUcHTURWcUQc[SUR[cHSc^YcOU_WA'
x=[ord(j) for j in x]
y=''

for p in x:
    y += chr(p^0x3c)

print y
