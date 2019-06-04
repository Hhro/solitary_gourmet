import string

key='4-EZF2M-7O5F4-V9P7O-EVFDP-E4VDO-O'
####'h sctf{ k3ith _m4k3 s_tr4 sh_r3 }'
base='hsctf{k3ith_m4k3s_tr4sh_r3}'
case='ABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890'


for x in key:
	if x == '-':
		continue

	idx = case.index(x)
	res = x+' : '
	k=0

	while (idx + len(case)*k):
		c = idx + len(case)*k

		if c>=256:
			break

		res += chr(c)
		k+=1

		if idx + len(case)*k ==idx:
			break

	print res
