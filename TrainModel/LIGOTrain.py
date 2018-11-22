from learn_Scientific import RLagent_Scientific
from Env.Environment import Environment, Workflow
from ScientificWorkflow.XMLProcess import XMLtoDAG
import copy

taskCount = 30
alpha = 0.6
DAG = XMLtoDAG("../ScientificWorkflow/LIGO_30.xml", taskCount=taskCount).getDAG()
montageWorklfow = Workflow(taskCount=taskCount, alpha=alpha, DAG=DAG)
env = Environment(taskCount=taskCount, alpha=alpha, workflow=montageWorklfow)


mt = RLagent_Scientific(env, taskCount, alpha, hiddenSize=80, perfix='LIGO')
mt.epsilon = 0.3
mt.epsilon_end = 0.05
mt.epsilon_decay = 200

mt.train()
