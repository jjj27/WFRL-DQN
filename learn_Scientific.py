from model import DQN
import torch
import torch.autograd as autograd
import torch.optim as optim
import numpy as np
from Env.Environment import Environment
from memory import MemoryReplay
import time
from utils import (sample_action, save_statistic)
import math


class RLagent_Scientific:

    def __init__(self, env, taskCount = 100, alpha = 0.4, hiddenSize = 500, perfix=''):
        self.GAMMA = 0.99
        self.epsilon = 0.3
        self.epsilon_end = 0.05
        self.epsilon_decay = 200
        self.update_step = 20
        self.memory_size = 2000
        self.max_epoch = 1000
        self.batch_size = 32
        self.hiddenSize = hiddenSize
        # self.save_path = '../Model/' + str(taskCount) + '-' + str(alpha) + perfix +'.pth'
        self.save_path = '../Model/' + perfix + '-' + str(taskCount) + '-' + str(alpha) +'.pth'

        # Variables
        self.var_phi = autograd.Variable(torch.Tensor(6), volatile=True)

        # For training
        self.var_batch_phi = autograd.Variable(torch.Tensor(self.batch_size, 6))
        self.var_batch_a = autograd.Variable(torch.LongTensor(self.batch_size, 1), requires_grad=False)
        self.var_batch_r = autograd.Variable(torch.Tensor(self.batch_size, 1))
        self.var_batch_phi_next = autograd.Variable(torch.Tensor(self.batch_size, 6))
        self.var_batch_r_mask = autograd.Variable(torch.Tensor(self.batch_size, 1), requires_grad=False)

        self.MP = MemoryReplay(self.memory_size, self.batch_size)
        self.dqn = DQN(hiddenSize=self.hiddenSize)
        self.target_dqn = DQN(hiddenSize=self.hiddenSize)
        self.target_dqn.load_state_dict(self.dqn.state_dict())

        self.optimz = optim.RMSprop(self.dqn.parameters(),  lr=0.00025, alpha=0.9, eps=1e-02, momentum=0.0)

        self.env = env

    def memoryInit(self):
        print("================\n" 
              "Replay Memory initlization!!\n"
              "================")
        i = 0
        while i < self.memory_size:
            taskNos = self.env.getNewTasks()
            if len(taskNos) == 0:
                self.env.spanTimeProcess()
            else:
                for taskNo in taskNos:
                    action = np.random.randint(0, 5)
                    vmPerm = self.env.scheduleTask(taskNo, action)
                    ob = self.env.getObservation(vmPerm = vmPerm)
                    done, r = self.env.isDone()
                    self.MP.put((ob, action, r, done))
                    i= i + 1
                self.env.spanTimeProcess()
            done, r = self.env.isDone()
            if done:
                ob = self.env.getObservation()
                self.MP.put((ob, action, r, done))
                # self.env.reset(newWorkflow=True)
                self.env.reset2()

    def train(self):
        self.memoryInit()
        print("================\n" 
        	  "Start training!!\n"
        	  "================")

        # self.env.reset(newWorkflow=True)
        self.env.reset2()

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

        while(epoch < self.max_epoch):
            ep = self.epsilon_end + (self.epsilon - self.epsilon_end) * math.exp(-1. * epoch / self.epsilon_decay)
            done = False
            actions = []
            while not done:
                self.optimz.zero_grad()

                taskNos = self.env.getNewTasks()
                if len(taskNos) == 0:
                    self.env.spanTimeProcess()
                else:
                    for taskNo in taskNos:
                        action = sample_action(self.env, self.dqn, self.var_phi, ep)
                        vmPerm = self.env.scheduleTask(taskNo, action)
                        actions.append(action)
                        ob = self.env.getObservation(vmPerm=vmPerm)
                        done, r = self.env.isDone()
                        self.MP.put((ob, action, r, done))
                    self.env.spanTimeProcess()
                done, r = self.env.isDone()
                if done:
                    ob = self.env.getObservation()
                    self.MP.put((ob, action, r, done))
                score += r

                # batch sample from memory to train
                batch_phi, batch_a, batch_r, batch_phi_next, batch_done = self.MP.batch()
                self.var_batch_phi_next.data.copy_(torch.from_numpy(batch_phi_next))
                batch_target_q, _ = self.target_dqn(self.var_batch_phi_next).max(dim=1)

                mask_index = np.ones((self.batch_size, 1))
                mask_index[batch_done] = 0.0
                self.var_batch_r_mask.data.copy_(torch.from_numpy(mask_index))

                self.var_batch_r.data.copy_(torch.from_numpy(batch_r))

                y = self.var_batch_r + batch_target_q.mul(self.GAMMA).mul(self.var_batch_r_mask)
                y = y.detach()

                self.var_batch_phi.data.copy_(torch.from_numpy(batch_phi))
                batch_q = self.dqn(self.var_batch_phi)

                self.var_batch_a.data.copy_(torch.from_numpy(batch_a).long().view(-1, 1))
                batch_q = batch_q.gather(1, self.var_batch_a)

                loss = y.sub(batch_q).pow(2).mean()
                loss.backward()
                self.optimz.step()

                update_count += 1

                if update_count == self.update_step:
                    self.target_dqn.load_state_dict(self.dqn.state_dict())
                    update_count = 0

                QVALUE.append(batch_q.data.cpu().numpy().mean())

            SCORE.append(score)
            QVALUE_MEAN.append(np.mean(QVALUE))
            QVALUE_STD.append(np.std(QVALUE))
            QVALUE = []

            epoch += 1
            avg_score = 0.9*avg_score + 0.1*score

            #print(actions)
            #print(avg_score, self.env.currentTime, self.env.workflow.DeadLine)
            print(avg_score)
            score = 0.0
            # self.env.reset(newWorkflow=True)
            self.env.reset2()

            time_elapse = time.time() - t

            #if avg_score >= best_score and time_elapse > 60:
            # if avg_score >= best_score:
            #     torch.save(self.dqn.state_dict(), self.save_path)
            #     print('Model has been saved.')
            #     best_score = avg_score
            #     t = time.time()
        torch.save(self.dqn.state_dict(), self.save_path)
        print('Model has been saved.')

        print()
        print('QVALUE_STD')
        print(QVALUE_STD)

        print()
        print('QVALUE_MEAN')
        print(QVALUE_MEAN)
