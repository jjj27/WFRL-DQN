from model import DQN
import torch
import torch.autograd as autograd
from utils import sample_action
import numpy as np
import pickle

# Montage: 25
# Cybershake: 30
# Epig: 24
# Random: 30
# LIGO: 30

algo = 'DeepWS'
wf = 'LIGO'
alpha = 0.6
taskCount = 30
dataset = './ScientificWorkflow/' + wf + '-' + str(alpha) + '-ENVs'
model = './Model/' + wf + '-' + str(taskCount) + '-' + str(alpha) + '.pth'


with open(dataset, 'rb') as file:
	ENVs = pickle.load(file)
done = False

the_model = torch.load(model, map_location='cpu')
dqn = DQN(hiddenSize=60)
dqn.load_state_dict(the_model)

var_phi = autograd.Variable(torch.Tensor(6), volatile=True)

RL_fail = 0
times = []
costs = []
VMtypes = []
for i in range(len(ENVs)):
# for i in range(2):
    env = ENVs[i]

    RL_actions = []
    while True:
        taskNos = env.getNewTasks()
        if len(taskNos) == 0:
            env.spanTimeProcess()
            # curCost = env.timeProcess()
            # costs.append(curCost)

        else:
            for taskNo in taskNos:
                vmType = sample_action(env, dqn, var_phi, epsilon=0)
                # vmType = 4
                RL_actions.append(vmType)
                # vmType = np.random.randint(0,5)
                env.scheduleTask(taskNo, vmType)
            curCost = env.timeProcess()
            # costs.append(curCost)

        # done, r = env.isDone()
        done, r = env.isDone2()
        if done:
            # f = open("heatmap/DeepWS.txt", "a")
            # s = ''
            # # print('Costs: ', costs)
            # for c in costs:
            #     s = s + str(c) + ' '
            # print(s, file=f)
            # f.close()
            # print('RL_actions: ', RL_actions)
            # print('ExecutionTime: ', env.currentTime)
            # print('Reward: ', r)
            # print('Cost: ', env.totalCost)
            # print()
            
            #types = []
            #for i in range(5):
            #    types.append(RL_actions.count(i))
            #VMtypes.append(types)
            # print('RL_actions: ', RL_actions)
            # print('count: ', types)
            
            print(env.currentTime, env.totalCost)
            times.append(env.currentTime)
            costs.append(env.totalCost)
            if r < 0:
                RL_fail += 1
            # else:
            #     RL_cost.append(env.totalCost)
            break

print('RL_fail: ', np.mean(RL_fail))
if len(costs) == 0:
    print('RL_cost_mean: N/A')
else:
    print('RL_cost_mean: ', np.mean(costs))
    
print('RL_time_mean: ', np.mean(times))

filename = "PlayOutput/" + wf + '-' + str(alpha) + '-' + algo + '.txt'
f = open(filename, "w")
f.truncate()
f.close()

f = open(filename, "a")
s = ''

for i in range(len(times)):
    print(times[i], costs[i], file=f)
f.close()

#AvgTypes = []
#for i in range(5):
#    curTs = 0
#    l = len(VMtypes)
#    for j in range(l):
#        curTs += VMtypes[j][i]
#    AvgTypes.append(curTs / l)
#print(AvgTypes)
    
