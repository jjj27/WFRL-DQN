from model import DQN
from Env.Environment import Environment
import torch
import torch.autograd as autograd
from utils import sample_action
import numpy as np
from ICPCP import ICPCP
import pickle


algo = 'SCS'
wf = 'Random'
alpha = 0.8
dataset = './ScientificWorkflow/' + wf + '-' + str(alpha) + '-ENVs'
with open(dataset, 'rb') as file:
	ENVs = pickle.load(file)
 
 
# env = Environment(taskCount=100, alpha=0.5)
# with open('./ScientificWorkflow/Random-0.8-ENVs', 'rb') as file:
# 	ENVs = pickle.load(file)
# done = False

Heur_fail = 0
Heur_cost = []
costs = []
times = []

for i in range(len(ENVs)):
    actions = []
    env = ENVs[i]
    while True:
        taskNos = env.getNewTasks()
        if len(taskNos) == 0:
            # env.timeProcess()
            env.spanTimeProcess()
        else:
            for taskNo in taskNos:
                ob = env.getObservation()
                if ob[0] < ob[5]:
                    vmType = 0
                elif ob[1] < ob[5]:
                    vmType = 1
                elif ob[2] < ob[5]:
                    vmType = 2
                elif ob[3] < ob[5]:
                    vmType = 3
                else:
                    vmType = 4
                actions.append(vmType)
                env.scheduleTask(taskNo, vmType)
            env.timeProcess()
        done, reward = env.isDone()

        if done:
            # print('RL:', r)
            print(env.currentTime, env.totalCost)
            if reward < 0:
                Heur_fail += 1
            # else:
            # print('Actins:', actions)
            # print('DeadLine:', env.workflow.DeadLine, ' Makespan: ', env.currentTime)
            # print()
            # Heur_cost.append(env.totalCost)
            costs.append(env.totalCost)
            times.append(env.currentTime)
            break
    env.reset(newWorkflow=True)

# print('Random_fail: ', np.mean(Heur_fail))
print('SCS_fail: ', np.mean(Heur_fail))
print('SCS_cost_mean: ', np.mean(costs))

filename = "PlayOutput/" + wf + '-' + str(alpha) + '-' + algo + '.txt'

f = open(filename, "w")
f.truncate()
f.close()

f = open(filename, "a")
s = ''

for i in range(len(times)):
    print(times[i], costs[i], file=f)
f.close()
# print('Random_cost_mean: ', np.mean(Heur_cost))