#!/usr/bin/python
# -*- coding: UTF-8 -*-

from ScientificWorkflow.XMLProcess import XMLtoDAG
from Env.Workflow import Workflow
from Env.Environment import Environment
import numpy as np
import pickle

alpha = 0.2
ENVs = []

taskCount = 30
DAG = np.zeros((taskCount, taskCount))
DAG[0,2] = 1
DAG[0,3] = 1
DAG[0,4] = 1
DAG[0,5] = 1
DAG[0,6] = 1

DAG[1,7] = 1
DAG[1,8] = 1
DAG[1,9] = 1
DAG[1,10] = 1
DAG[1,11] = 1
DAG[1,12] = 1
DAG[1,13] = 1
DAG[1,14] = 1

DAG[2,20] = 1
DAG[3,20] = 1
DAG[4,20] = 1
DAG[5,20] = 1
DAG[6,20] = 1
DAG[7,20] = 1
DAG[8,20] = 1
DAG[9,20] = 1
DAG[10,20] = 1
DAG[11,20] = 1
DAG[12,20] = 1
DAG[13,20] = 1
DAG[14,20] = 1

DAG[2,15] = 1
DAG[3,16] = 1
DAG[4,17] = 1
DAG[5,18] = 1
DAG[6,19] = 1

DAG[7,21] = 1
DAG[8,22] = 1
DAG[9,23] = 1
DAG[10,24] = 1
DAG[11,25] = 1
DAG[12,26] = 1
DAG[13,27] = 1
DAG[14,28] = 1

DAG[15,29] = 1
DAG[16,29] = 1
DAG[17,29] = 1
DAG[18,29] = 1
DAG[19,29] = 1
DAG[20,29] = 1
DAG[21,29] = 1
DAG[22,29] = 1
DAG[23,29] = 1
DAG[24,29] = 1
DAG[25,29] = 1
DAG[26,29] = 1
DAG[27,29] = 1
DAG[28,29] = 1




for i in range(100):
	CybershakeWorklfow = Workflow(taskCount=taskCount, alpha=alpha, DAG=DAG)
	env = Environment(taskCount=taskCount, save=False, alpha=alpha, workflow=CybershakeWorklfow)
	ENVs.append(env)

dbfile = open('Cybershake-'+str(alpha)+'-ENVs', 'wb')
pickle.dump(ENVs, dbfile)
dbfile.close()






#name = 'Epig'
#alpha = 0.8
#ENVs = []
#DAG = XMLtoDAG("Epigenomics_24.xml", taskCount=24).getDAG()
#
#for i in range(100):
#	SCWorklfow = Workflow(taskCount=24, alpha=alpha, DAG=DAG)
#	env = Environment(taskCount=24, save=False, alpha=alpha, workflow=SCWorklfow)
#	ENVs.append(env)
#
#dbfile = open(name+'-'+str(alpha)+'-ENVs', 'wb')
#pickle.dump(ENVs, dbfile)
#dbfile.close()