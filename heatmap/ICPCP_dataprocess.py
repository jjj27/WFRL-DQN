#!/usr/bin/python3
# 打开文件
fo = open("ICPCP.txt", "r")

ll = []
for line in fo.readlines():  # 依次读取每行
	l = line.split()
	ls = []
	for e in l:
		ls.append(float(e))
	ll.append(ls)

fo.close()

lp = []
for i in range(len(ll)):
	ls = ll[i]
	interval = len(ls) / 100
	cindex = 0
	curC = 0
	lc = []
	for index in range(len(ls)):
		if int(index / interval) != cindex:
			lc.append(curC)
			curC = 0
			cindex = int(index / interval)
		else:
			curC = curC + ls[index]
	lc.append(curC)
	# print(len(lc))
	# print(lc)
	lp.append(lc)


cc = []
for i in range(100):
	c = 0
	for j in range(100):
		c = c + lp[j][i]
	c = c / 100
	cc.append(c)

f = open("ICPCP_processed.txt", "a")
s = ''
for c in cc:
	s = s + str(c) + ' '
print(s, file=f)
f.close()

# f = open("montage_processed.txt", "a")
#
#
#
# for i in range(len(lp)):
# 	lc = lp[i]
# 	s = ''
# 	for c in lc:
# 		s = s + str(c) + ' '
# 	print(s, file=f)
#
# f.close()
#
#
#