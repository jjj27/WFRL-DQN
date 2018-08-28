from model import DQN
from Env.Environment import Environment
import torch
import torch.autograd as autograd
from utils import sample_action
import numpy as np
from ICPCP import ICPCP


the_model = torch.load('./tmp/100-0.8.pth', map_location='cpu')

dqn = DQN()
dqn.load_state_dict(the_model)

env = Environment(taskCount=100, alpha=0.8)
done = False

var_phi = autograd.Variable(torch.Tensor(6), volatile=True)

RL_fail = 0
RL_cost = []
Random_fail = 0
Random_cost = []
for i in range(100):
    RL_actions = []
    He_actions = []
    while True:
        taskNos = env.getNewTasks()
        if len(taskNos) == 0:
            env.spanTimeProcess()
            done, r = env.isDone()
        else:
            for taskNo in taskNos:
                vmType = sample_action(env, dqn, var_phi, epsilon=0)
                RL_actions.append(vmType)
                # vmType = np.random.randint(0,3)
                done, reward = env.step(taskNo, vmType)

        if done:
            print('RL_actions: ', RL_actions)
            if r < 0:
                RL_fail += 1
            else:
                RL_cost.append(env.totalCost)
            break


    env.reset(newWorkflow=False)
    while True:
        taskNos = env.getNewTasks()
        if len(taskNos) == 0:
            env.spanTimeProcess()
            done, r = env.isDone()
        else:
            for taskNo in taskNos:
                #vmType = np.random.randint(0, 3)
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
                He_actions.append(vmType)
                done, reward = env.step(taskNo, vmType)

        if done:
            print('He_actions: ', He_actions)
            print()
            if r < 0:
                Random_fail += 1
            else:
                Random_cost.append(env.totalCost)
            break
    env.reset(newWorkflow=True)

print('RL_fail: ', np.mean(RL_fail))
print('RL_cost_mean: ', np.mean(RL_cost))

print('Random_fail: ', np.mean(Random_fail))
print('Random_cost_mean: ', np.mean(Random_cost))