import numpy as np

wfs = ['Montage', 'Cybershake', 'Epig', 'Random', 'LIGO']
alphas = [0.2, 0.4, 0.6, 0.8]
algos = ['DeepWS', 'SCS', 'PSO', 'ICPCP']

deadlines = []
for wf in wfs:
	savename = "./DLhit-rate-" + wf
	f = open(savename, "w")
	f.truncate()
	f.close()
	f = open(savename, "a")
	print('algorithm', '0.2', '0.4', '0.6', '0.8', file=f)
	
	hitt = []
	for alpha in alphas:
		filename = "../PlayOutput/" + wf + '-' + str(alpha) + '-Deadline.txt'
		fr = open(filename, 'r')
		lines = fr.readlines()
		dl = []
		for line in lines:
			line = line.rstrip('\n')
			dl.append(float(line))
		fr.close()
		
		hitrates = []
		for algo in algos:
			filename = "../PlayOutput/" + wf + '-' + str(alpha) + '-' + algo + '.txt'
			fr = open(filename, 'r')
			lines = fr.readlines()
			times = []
			for line in lines:
				line = line.rstrip('\n').split(' ')
				times.append(float(line[0]))
			fr.close()
		
			hitcount = 0
			for i in range(len(times)):
				if times[i] < dl[i]:
					hitcount = hitcount + 1
			hitrates.append(hitcount)
		hitt.append(hitrates)
	
	print('DeepWS', hitt[0][0], hitt[1][0], hitt[2][0], hitt[3][0], file=f)
	print('SCS',    hitt[0][1], hitt[1][1], hitt[2][1], hitt[3][1], file=f)
	print('PSO',    hitt[0][2], hitt[1][2], hitt[2][2], hitt[3][2], file=f)
	print('ICPCP',  hitt[0][3], hitt[1][3], hitt[2][3], hitt[3][3], file=f)
				
		
			