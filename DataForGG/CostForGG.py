import numpy as np

wfs = ['Montage', 'Cybershake', 'Epig', 'Random', 'LIGO']
alphas = [0.2, 0.4, 0.6, 0.8]
algos = ['DeepWS', 'SCS', 'PSO', 'ICPCP']

for wf in wfs:
	savename = "./Cost-" + wf
	f = open(savename, "w")
	f.truncate()
	f.close()
	f = open(savename, "a")
	
	print('alphavalue', 'DeepWS_cost', 'DeepWS_penalty', 'SCS_cost',
	      'SCS_penalty', 'PSO_cost', 'PSO_penalty', 'IC-PCP_cost',
	      'IC-PCP_penalty', file=f)
	
	for alpha in alphas:
		filename = "../PlayOutput/" + wf + '-' + str(alpha) + '-Deadline.txt'
		fr = open(filename, 'r')
		lines = fr.readlines()
		dl = []
		for line in lines:
			line = line.rstrip('\n')
			dl.append(float(line))
		fr.close()
		
		print(alpha, ' ', end='', file=f)
		for algo in algos:
			filename = "../PlayOutput/" + wf + '-' + str(alpha) + '-' + algo + '.txt'
			fr = open(filename, 'r')
			lines = fr.readlines()
			times = []
			costs = []
			for line in lines:
				line = line.rstrip('\n').split(' ')
				times.append(float(line[0]))
				costs.append(float(line[1]))
			fr.close()
			
			pen = 0
			for i in range(len(times)):
				if times[i] > dl[i]: # 超时
					# pen = pen + (times[i] - dl[i]) * 4
					pen = pen + (times[i] - dl[i]) * 20
			
			oricost = np.mean(costs)
			if pen / len(times) > oricost * 0.3:
				pen = oricost * 0.3
			else:
				pen = pen / len(times)
				
			print(oricost, ' ',  pen, ' ',  end='', file=f)
		
		print("", file=f)
			
				
			

