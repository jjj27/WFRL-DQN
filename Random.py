from model import DQN
from Env.Environment import Environment
import torch
import torch.autograd as autograd
from utils import sample_action
import numpy as np
from ICPCP import ICPCP
import pickle

# model-3.pth     taskCount = 10
# model-4.pth     taskCount = 20
# model-5.pth     taskCount = 40

# env = Environment(taskCount=100, alpha=0.8)
with open('env-100', 'rb') as file:
	env = pickle.load(file)
	env.workflow.print()
done = False

Random_fail = 0
Random_cost = []

for i in range(20):
    actions = []
    while True:
        taskNos = env.getNewTasks()
        if len(taskNos) == 0:
            env.spanTimeProcess()
            done, r = env.isDone()
        else:
            for taskNo in taskNos:
                vmType = np.random.randint(0, 5)
                actions.append(vmType)
                done, reward = env.step(taskNo, vmType)

        if done:
            # print('RL:', r)
            if r < 0:
                Random_fail += 1
            else:
                print('Actins:', actions)
                print('DeadLine:', env.workflow.DeadLine, ' Makespan: ', env.currentTime)
                print('Cost: ', env.totalCost)
                print()
                Random_cost.append(env.totalCost)
            break
    env.reset(newWorkflow=True)

print('Random_fail: ', np.mean(Random_fail))
print('Random_cost_mean: ', np.mean(Random_cost))