#!/usr/bin/python
# -*- coding: UTF-8 -*-

from ScientificWorkflow.XMLProcess import XMLtoDAG
from Env.Workflow import Workflow
from Env.Environment import Environment
import numpy as np
import pickle

taskCount = 25
alpha = 0.8
ENVs = []

with open('./Random-Origin', 'rb') as file:
	OriginWorkflow = pickle.load(file)

for i in range(100):
	env = Environment(taskCount=taskCount, save=False, alpha=alpha, workflow=OriginWorkflow[i].workflow)
	ENVs.append(env)

dbfile = open('Random-'+str(alpha)+'-ENVs', 'wb')
pickle.dump(ENVs, dbfile)
dbfile.close()