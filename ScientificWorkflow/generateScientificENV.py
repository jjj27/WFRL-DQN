#!/usr/bin/python
# -*- coding: UTF-8 -*-

from ScientificWorkflow.XMLProcess import XMLtoDAG
from Env.Workflow import Workflow
from Env.Environment import Environment
import numpy as np
import pickle

taskCount = 30
alpha = 0.8
ENVs = []

with open('./LIGO-Origin', 'rb') as file:
	OriginWorkflow = pickle.load(file)

for i in range(100):
	# used for other
	env = Environment(taskCount=taskCount, save=False, alpha=alpha, workflow=OriginWorkflow[i].workflow)
	
	# used for LIGO
	# env = Environment(taskCount=taskCount, save=False, alpha=alpha, workflow=OriginWorkflow[i])
	ENVs.append(env)

dbfile = open('LIGO-'+str(alpha)+'-ENVs', 'wb')
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