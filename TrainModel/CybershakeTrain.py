from learn_Scientific import RLagent_Scientific
from Env.Environment import Environment, Workflow
from ScientificWorkflow.XMLProcess import XMLtoDAG
import copy

taskCount = 30
alpha = 0.4
DAG = XMLtoDAG("../ScientificWorkflow/CyberShake_30.xml", taskCount=taskCount).getDAG()
montageWorklfow = Workflow(taskCount=taskCount, alpha=alpha, DAG=DAG)
env = Environment(taskCount=taskCount, alpha=alpha, workflow=montageWorklfow)


mt = RLagent_Scientific(env, taskCount, alpha, hiddenSize=80, perfix='CyberShake')
mt.epsilon = 0.3
mt.epsilon_end = 0.05
mt.max_epoch = 1000
mt.train()