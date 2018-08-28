from learn_Scientific import RLagent_Scientific
from Env.Environment import Environment, Workflow
from ScientificWorkflow.XMLProcess import XMLtoDAG
import copy

taskCount = 24
alpha = 0.8
DAG = XMLtoDAG("../ScientificWorkflow/Epigenomics_24.xml", taskCount=taskCount).getDAG()
montageWorklfow = Workflow(taskCount=taskCount, alpha=alpha, DAG=DAG)
env = Environment(taskCount=taskCount, alpha=alpha, workflow=montageWorklfow)


mt = RLagent_Scientific(env, taskCount, alpha, hiddenSize=60, perfix='Epigenomics')
mt.epsilon = 0.3
mt.epsilon_end = 0.05
mt.max_epoch = 1000
mt.train()