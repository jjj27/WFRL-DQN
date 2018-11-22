from learn_Scientific import RLagent_Scientific
from Env.Environment import Environment, Workflow
from ScientificWorkflow.XMLProcess import XMLtoDAG
import copy

taskCount = 25
alpha = 0.2
DAG = XMLtoDAG("../ScientificWorkflow/Montage_25.xml", taskCount=taskCount).getDAG()
montageWorklfow = Workflow(taskCount=taskCount, alpha=alpha, DAG=DAG)
env = Environment(taskCount=taskCount, alpha=alpha, workflow=montageWorklfow)


mt = RLagent_Scientific(env, taskCount, alpha, hiddenSize=80, perfix='Montage')
mt.epsilon = 0.3
mt.epsilon_end = 0.05
mt.epsilon_decay = 200

mt.train()
