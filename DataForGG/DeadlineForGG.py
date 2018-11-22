import numpy as np

wfs = ['Montage', 'Cybershake', 'Epig', 'Random', 'LIGO']
alphas = [0.2, 0.4, 0.6, 0.8]

for wf in wfs:
	savename = "./AverageDeadline-" + wf
	f = open(savename, "w")
	f.truncate()
	f.close()
	f = open(savename, "a")
	print('alphavalue', 'deadline', file=f)
	for alpha in alphas:
		filename = "../PlayOutput/" + wf + '-' + str(alpha) + '-Deadline.txt'
		fr = open(filename, 'r')
		lines = fr.readlines()
		dl = []
		for line in lines:
			line = line.rstrip('\n')
			dl.append(float(line))
		fr.close()
		
		print(alpha, np.mean(dl), file=f)
		
			