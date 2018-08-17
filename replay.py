from model import DQN
from Env.Environment import Environment
import torch
import torch.autograd as autograd
from utils import sample_action
import numpy as np

# model-3.pth     taskCount = 10
# model-4.pth     taskCount = 20
# model-5.pth     taskCount = 40

the_model = torch.load('./tmp/model-3.pth', map_location='cpu')

dqn = DQN()
dqn.load_state_dict(the_model)

env = Environment(taskCount=10)
done = False

VALID_ACTION = [0, 1, 2]
var_phi = autograd.Variable(torch.Tensor(4), volatile=True)





for j in range(100):
    RL_fail = 0
    Random_fail = 0
    RL_cost = []
    Random_cost = []

    for i in range(100):
        while True:
            ob = env.getObservation()
            taskNo = env.getTaskToSchedule()
            act_index = sample_action(env, dqn, var_phi, epsilon=0)
            ob, r, done, succ = env.step(taskNo, vmType=VALID_ACTION[act_index])

            if done:
                # print('RL:', r)
                if env.workflowbak.DeadLine - env.currentTime < 0:
                    RL_fail += 1
                else:
                    RL_cost.append(env.totalCost)
                break


        env.reset(newWorkflow=False)

        while True:
            ob = env.getObservation()
            taskNo = env.getTaskToSchedule()
            act_index = np.random.randint(0, 3)
            ob, r, done, succ = env.step(taskNo, vmType=VALID_ACTION[act_index])

            if done:
                # print('Random:', r)
                if env.workflowbak.DeadLine - env.currentTime < 0:
                    Random_fail += 1
                else:
                    Random_cost.append(env.totalCost)
                break

        env.reset(newWorkflow=True)


    print()
    print('RL_fail: ', RL_fail)
    print('Random_fail: ', Random_fail)

    print('RL_cost_mean: ', np.mean(RL_cost))
    print('Random_cost_mean: ', np.mean(Random_cost))