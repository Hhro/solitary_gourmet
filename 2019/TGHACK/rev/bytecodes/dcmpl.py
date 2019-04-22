# uncompyle6 version 3.3.0
# Python bytecode 3.6 (3379)
# Decompiled from: Python 2.7.12 (default, Nov 12 2018, 14:36:49) 
# [GCC 5.4.0 20160609]
# Embedded file name: main.py
# Compiled at: 2019-04-13 21:56:41
# Size of source mod 2**32: 514 bytes
import binascii, sys

def print_flag():
    enc = '1605737b39323b362a2d2c1d203b3627212d26271d2b2c1d362a271d2a2d3731273f'
    enc = binascii.unhexlify(enc)
    key = 66
    dec = ''
    for i in enc:
        dec += chr(i ^ key)

    print(dec)


def main(code):
    if code == 1337:
        print_flag()
    else:
        print('wrong!')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('error! missing magic code!')
        sys.exit()
    main(int(sys.argv[1]))
# okay decompiling main.pyc
