from learn_Scientific import RLagent_Scientific
from Env.Environment import Environment, Workflow
from ScientificWorkflow import generateCybershakeENV
from ScientificWorkflow.XMLProcess import XMLtoDAG
import copy
import numpy as np

taskCount = 30
alpha = 0.6
DAG = generateCybershakeENV.CybershakeDAGGen.getDAG()
wf = Workflow(taskCount=taskCount, alpha=alpha, DAG=DAG)
env = Environment(taskCount=taskCount, alpha=alpha, workflow=wf)


mt = RLagent_Scientific(env, taskCount, alpha, hiddenSize=80, perfix='CyberShake')
mt.epsilon = 0.3
mt.epsilon_end = 0.05
mt.epsilon_decay = 200
mt.train()