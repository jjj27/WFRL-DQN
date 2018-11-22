from model import DQN
from Env.Environment import Environment
import torch
import torch.autograd as autograd
from utils import sample_action
import numpy as np
import pickle



algo = 'DeepWS'
wf = 'Random'
alpha = 0.8
dataset = './ScientificWorkflow/' + wf + '-' + str(alpha) + '-ENVs'
model = './Model/Random-30-' + str(alpha) + '.pth'



with open(dataset, 'rb') as file:
	ENVs = pickle.load(file)
done = False
the_model = torch.load(model, map_location='cpu')

dqn = DQN()
dqn.load_state_dict(the_model)



var_phi = autograd.Variable(torch.Tensor(6), volatile=True)

RL_fail = 0
RL_cost = []
times = []
costs = []
for i in range(len(ENVs)):
    env = ENVs[i]
    RL_actions = []
    while True:
        taskNos = env.getNewTasks()
        if len(taskNos) == 0:
            env.spanTimeProcess()

        else:
            for taskNo in taskNos:
                vmType = sample_action(env, dqn, var_phi, epsilon=0)
                RL_actions.append(vmType)
                # vmType = np.random.randint(0,3)
                env.scheduleTask(taskNo, vmType)
            env.timeProcess()
        done, r = env.isDone2()
        if done:
            # print('DeadLine: ', env.workflow.DeadLine)
            # print('RL_actions: ', RL_actions)
            # print('ExecutionTime: ', env.currentTime)
            # print('Cost: ', env.totalCost)
            # print()
            print(env.currentTime, env.totalCost)
            times.append(env.currentTime)
            costs.append(env.totalCost)
            if r < 0:
                RL_fail += 1
            # else:
            #     RL_cost.append(env.totalCost)
            break

    env.reset(newWorkflow=True)

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
