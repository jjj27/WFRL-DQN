import numpy as np
from ICPCP import ICPCP
import pickle

wf = 'LIGO'
alpha = 0.8
dataset = './ScientificWorkflow/' + wf + '-' + str(alpha) + '-ENVs'
with open(dataset, 'rb') as file:
	ENVs = pickle.load(file)
	
	
filename = "PlayOutput/" + wf + '-' + str(alpha) + '-Deadline.txt'

f = open(filename, "w")
f.truncate()
f.close()

f = open(filename, "a")
s = ''


for env in ENVs:
	print(env.workflow.DeadLine, file=f)
f.close()