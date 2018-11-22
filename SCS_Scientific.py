from model import DQN
from Env.Environment import Environment, Workflow
import torch
import torch.autograd as autograd
from utils import sample_action
import numpy as np
from ICPCP import ICPCP
import pickle
from ScientificWorkflow.XMLProcess import XMLtoDAG

algo = 'SCS'
wf = 'LIGO'
alpha = 0.8
dataset = './ScientificWorkflow/' + wf + '-' + str(alpha) + '-ENVs'
with open(dataset, 'rb') as file:
	ENVs = pickle.load(file)

done = False

Heur_fail = 0
Heur_cost = []

VMtypes = []
times = []
costs = []

for i in range(len(ENVs)):
    actions = []
    env = ENVs[i]
    # costs = []
    while True:
        taskNos = env.getNewTasks()
        if len(taskNos) == 0:
            #curCost = env.timeProcess()
            #costs.append(curCost)
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
            # env.timeProcess()
            curCost = env.timeProcess()
            #costs.append(curCost)
        done, reward = env.isDone2()

        if done:
            # f = open("heatmap/SCS.txt", "a")
            # s = ''
            # for c in costs:
            #     s = s + str(c) + ' '
            # print(s, file=f)
            # f.close()
            types = []
            for i in range(5):
                types.append(actions.count(i))
            VMtypes.append(types)
            
            print(env.currentTime, env.totalCost)
            times.append(env.currentTime)
            costs.append(env.totalCost)
            if reward < 0:
                Heur_fail += 1
            # print('Actins:', actions)
            #print('DeadLine:', env.workflow.DeadLine, ' Makespan: ', env.currentTime)
            #print()
            #Heur_cost.append(env.totalCost)
            break
    env.reset2()

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
# AvgTypes = []
# for i in range(5):
#     curTs = 0
#     l = len(VMtypes)
#     for j in range(l):
#         curTs += VMtypes[j][i]
#     AvgTypes.append(curTs / l)
# print(AvgTypes)