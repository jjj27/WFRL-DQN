from model import DQN
from Env.Environment import Environment
import torch
import torch.autograd as autograd
from utils import sample_action
import numpy as np
import pickle

# model-3.pth     taskCount = 10
# model-4.pth     taskCount = 20
# model-5.pth     taskCount = 40
# model-6.pth     taskCount = 50


with open('./ScientificWorkflow/Random-0.8-ENVs', 'rb') as file:
	ENVs = pickle.load(file)
done = False
the_model = torch.load('./Model/Random-25-0.8.pth', map_location='cpu')

dqn = DQN()
dqn.load_state_dict(the_model)



var_phi = autograd.Variable(torch.Tensor(6), volatile=True)

RL_fail = 0
RL_cost = []
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
            if r < 0:
                RL_fail += 1
            else:
                RL_cost.append(env.totalCost)
            break

    env.reset(newWorkflow=True)

print('RL_fail: ', np.mean(RL_fail))
if len(RL_cost) == 0:
    print('RL_cost_mean: N/A')
else:
    print('RL_cost_mean: ', np.mean(RL_cost))
