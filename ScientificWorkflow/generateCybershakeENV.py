#!/usr/bin/python
# -*- coding: UTF-8 -*-

from ScientificWorkflow.XMLProcess import XMLtoDAG
from Env.Workflow import Workflow
from Env.Environment import Environment
import numpy as np
import pickle

class CybershakeDAGGen:
	
	@classmethod
	def getDAG(cls):
		
		taskCount = 30
		DAG = np.zeros((taskCount, taskCount))
		DAG[0, 1] = 1
		DAG[0, 2] = 1
		
		DAG[1, 3] = 1
		DAG[1, 4] = 1
		DAG[1, 5] = 1
		DAG[1, 6] = 1
		DAG[1, 7] = 1
		
		DAG[2, 8] = 1
		DAG[2, 9] = 1
		DAG[2, 10] = 1
		DAG[2, 11] = 1
		DAG[2, 12] = 1
		DAG[2, 13] = 1
		DAG[2, 14] = 1
		DAG[2, 15] = 1
		
		DAG[3, 16] = 1
		DAG[4, 17] = 1
		DAG[5, 18] = 1
		DAG[6, 19] = 1
		DAG[7, 20] = 1
		
		DAG[8, 21] = 1
		DAG[9, 22] = 1
		DAG[10, 23] = 1
		DAG[11, 24] = 1
		DAG[12, 25] = 1
		DAG[13, 26] = 1
		DAG[14, 27] = 1
		DAG[15, 28] = 1
		
		DAG[16, 29] = 1
		DAG[17, 29] = 1
		DAG[18, 29] = 1
		DAG[19, 29] = 1
		DAG[20, 29] = 1
		DAG[21, 29] = 1
		DAG[22, 29] = 1
		DAG[23, 29] = 1
		DAG[24, 29] = 1
		DAG[25, 29] = 1
		DAG[26, 29] = 1
		DAG[27, 29] = 1
		DAG[28, 29] = 1
		return DAG
		
	
	@classmethod
	def genDAG(cls, alpha = 0.2, taskCount = 30):
		ENVs = []
		DAG = CybershakeDAGGen.getDAG()
		for i in range(100):
			CybershakeWorklfow = Workflow(taskCount=taskCount, alpha=alpha, DAG=DAG)
			env = Environment(taskCount=taskCount, save=False, alpha=alpha, workflow=CybershakeWorklfow)
			ENVs.append(env)
		
		dbfile = open('Cybershake-'+str(alpha)+'-ENVs', 'wb')
		pickle.dump(ENVs, dbfile)
		dbfile.close()
		

if __name__ == '__main__':
	CybershakeDAGGen.genDAG(alpha=0.2)
	CybershakeDAGGen.genDAG(alpha=0.4)
	CybershakeDAGGen.genDAG(alpha=0.6)
	CybershakeDAGGen.genDAG(alpha=0.8)
	
	
	