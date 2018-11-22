

wfs = ['Montage', 'Cybershake', 'Epig', 'Random', 'LIGO']
alphas = [0.2, 0.4, 0.6, 0.8]
algos = ['DeepWS', 'SCS', 'PSO', 'ICPCP']





for wf in wfs:
	savename = "./" + wf
	f = open(savename, "w")
	f.truncate()
	f.close()
	f = open(savename, "a")
	print('Makespan', 'cost', 'algorithm', 'alphavalue', file=f)
	
	for alpha in alphas:
		for algo in algos:
			filename = "../PlayOutput/" + wf + '-' + str(alpha) + '-' + algo + '.txt'
			fr = open(filename, 'r')
			lines = fr.readlines()
			costs = []
			times = []
			for line in lines:
				line = line.rstrip('\n').split(' ')
				times.append(line[0])
				costs.append(line[1])
			fr.close()
			
			for i in range(len(costs)):
				print(times[i], costs[i], algo, alpha, file=f)
			
			
			
			


	
