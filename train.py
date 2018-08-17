from model import DQN
import torch
import torch.autograd as autograd
import torch.optim as optim

import numpy as np
import random

from Env.Environment import Environment
from memory import MemoryReplay

import time
from utils import (sample_action, save_statistic)
from collections import deque


VALID_ACTION = [0, 1, 2]
GAMMA = 0.99
epsilon = 0.05
update_step = 50
memory_size = 5000
max_epoch = 1000000
batch_size = 64
save_path = './tmp'

# EPS
EPS_START = 0.9
EPS_END = 0.5
EPS_DECAY = 200
steps_done = 0

# Variables
var_phi = autograd.Variable(torch.Tensor(4), volatile=True)

# For training
var_batch_phi = autograd.Variable(torch.Tensor(batch_size, 4))
var_batch_a = autograd.Variable(torch.LongTensor(batch_size, 1), requires_grad=False)
var_batch_r = autograd.Variable(torch.Tensor(batch_size, 1))
var_batch_phi_next = autograd.Variable(torch.Tensor(batch_size, 4))
var_batch_r_mask = autograd.Variable(torch.Tensor(batch_size, 1), requires_grad=False)


MP = MemoryReplay(memory_size, batch_size)
dqn = DQN()
target_dqn = DQN()
target_dqn.load_state_dict(dqn.state_dict())


optimz = optim.RMSprop(dqn.parameters(),  lr=0.00025, alpha=0.9, eps=1e-02, momentum=0.0)

env = Environment(taskCount=40)

print("================\n" 
	  "Replay Memory initlization!!\n"
	  "================")
i = 0
while i != memory_size:
    phi = env.getObservation()
    taskNo = env.getTaskToSchedule()


    act_index = random.randrange(3)
    action    = VALID_ACTION[act_index]
    ob, reward, done, succ = env.step(taskNo=taskNo, vmType=action)
    if succ:
        i = i + 1
        MP.put((ob, act_index, reward, done))

    if done:
        i = i + 1
        print(i)
        MP.put((ob, act_index, reward, done))
        env.reset(newWorkflow=True)

print("================\n" 
	  "Start training!!\n"
	  "================")

env.reset(newWorkflow=True)

epoch = 0
update_count = 0
score = 0.
avg_score = 0.
best_score = 0.

t = time.time()

SCORE = []
QVALUE = []
QVALUE_MEAN = []
QVALUE_STD = []

while(epoch < max_epoch): 

    while(not done):
        optimz.zero_grad()
        ob = env.getObservation()
        taskNo = env.getTaskToSchedule()

        act_index = sample_action(env, dqn, var_phi, epsilon)

        epsilon = (epsilon - 1e-3) if epsilon > 0.1 else  0.1

        ob, r, done, succ = env.step(taskNo, vmType=VALID_ACTION[act_index])

        if succ:
            MP.put((ob, act_index, r, done))

        r = np.clip(r, -1, 1)
        score += r

        # batch sample from memory to train
        batch_phi, batch_a, batch_r, batch_phi_next, batch_done = MP.batch()
        var_batch_phi_next.data.copy_(torch.from_numpy(batch_phi_next))
        batch_target_q, _ = target_dqn(var_batch_phi_next).max(dim=1)

        mask_index = np.ones((batch_size, 1))
        mask_index[batch_done] = 0.0
        var_batch_r_mask.data.copy_(torch.from_numpy(mask_index))
		
        var_batch_r.data.copy_(torch.from_numpy(batch_r))

        y = var_batch_r + batch_target_q.mul(GAMMA).mul(var_batch_r_mask)
        y = y.detach()

        var_batch_phi.data.copy_(torch.from_numpy(batch_phi))
        batch_q = dqn(var_batch_phi)

        var_batch_a.data.copy_(torch.from_numpy(batch_a).long().view(-1, 1))
        batch_q = batch_q.gather(1, var_batch_a)
		
        loss = y.sub(batch_q).pow(2).mean()
        loss.backward()
        optimz.step()

        update_count += 1

        if update_count == update_step:
            target_dqn.load_state_dict(dqn.state_dict())
            update_count = 0

        QVALUE.append(batch_q.data.cpu().numpy().mean())

    SCORE.append(score)
    QVALUE_MEAN.append(np.mean(QVALUE))
    QVALUE_STD.append(np.std(QVALUE))
    QVALUE = []

    #save_statistic('Score', SCORE, save_path=save_path)
    #save_statistic('Average Action Value', QVALUE_MEAN, QVALUE_STD, save_path)

    env.reset(newWorkflow=False)
    done = False
    epoch += 1
    avg_score = 0.9*avg_score + 0.1*score
    score = 0.0
    # print('Epoch: {0}. Avg.Score:{1:6f}'.format(epoch, avg_score))
    print(avg_score)

    time_elapse = time.time() - t

    if avg_score >= best_score and time_elapse > 60:
        torch.save(dqn.state_dict(), save_path+'/model-5.pth')
        print('Model has been saved.')
        best_score = avg_score
        t = time.time()
