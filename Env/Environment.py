#!/usr/bin/python
# -*- coding: utf8 -*-

from Env.Workflow import Workflow
from Env.VirtualMachine import VM
import pickle
import copy
import numpy as np

class Environment:

    def __init__(self, taskCount=10, save = False):
        self.taskCount = taskCount
        self.workflow  = Workflow(taskCount)
        self.workflowbak = copy.deepcopy(self.workflow)
        self.runningTasks  = []
        self.finishedTasks = []
        self.currentTime = 0
        self.resourcePool = []
        self.initVM()
        self.finishedSize = 0
        self.totalSize    = sum(self.workflow.taskSize)
        self.totalCost    = 0
        if save:
            dbfile = open('env-'+str(self.taskCount), 'wb')
            pickle.dump(self, dbfile)
            dbfile.close()

    def saveWorkflow(self):
        dbfile = open('env-' + str(self.taskCount), 'wb')
        pickle.dump(self, dbfile)
        dbfile.close()

    def getCurrentCost(self):
        cost = 0
        for vm in self.resourcePool:
            cost += vm.totalCost
        return cost

    def initVM(self):
        vm_large_1 = VM(speed=1.8, cost=2.5, type='large')
        vm_large_2 = VM(speed=1.8, cost=2.5, type='large')
        vm_large_3 = VM(speed=1.8, cost=2.5, type='large')

        vm_medium_1 = VM(speed=1.4, cost=1.7, type='medium')
        vm_medium_2 = VM(speed=1.4, cost=1.7, type='medium')
        vm_medium_3 = VM(speed=1.4, cost=1.7, type='medium')

        vm_small_1 = VM(speed=1, cost=1, type='small')
        vm_small_2 = VM(speed=1, cost=1, type='small')
        vm_small_3 = VM(speed=1, cost=1, type='small')

    def getFinishRate(self):
        return self.finishedSize / self.totalSize

    def timeProcess(self):
        self.currentTime += 0.1
        toRemove = []
        for i in range(len(self.resourcePool)):
            finishSig, cost = self.resourcePool[i].timeProcess(self)
            self.totalCost += cost
            if finishSig:
                self.setTaskFinished(self.resourcePool[i].taskNo)
                toRemove.append(self.resourcePool[i])
        self.resourcePool = [e for e in self.resourcePool if e not in toRemove]

    def step(self, taskNo, vmType):
        res, msg = self.scheduleTask(taskNo, vmType)
        succ = False
        reward = 0
        if res == 1:          # No available task to schedule!
            reward = 0
        elif res == 2:        # hold for current task
            reward = 0
        elif res == 4:        # schedule succ
            reward = 0
            succ = True

            # 正常步骤

        reward = 0

        self.timeProcess()
        ob = self.getObservation()
        done = False

        # 超时未完成
        if self.currentTime >= self.workflow.DeadLine:
            # reward = -1
            reward = -0.01
            done = True

        # 正常完成
        if len(self.finishedTasks) == self.workflow.taskCount:
            fastFinishTime = self.workflow.CPTime / 1.8
            finishTime = self.currentTime
            deadLine = self.workflow.DeadLine

            reward = (finishTime - fastFinishTime) / (deadLine - fastFinishTime)
            reward = reward * reward * reward
            done = True
            #print(reward)

        return ob, reward, done, succ

    def getObservation(self):
        obs = []
        taskNo = self.getTaskToSchedule()
        tasksize = self.workflow.taskSize[taskNo]
        obs.append(tasksize)
        obs.append(tasksize / 1.4)
        obs.append(tasksize / 1.8)
        # ratio = tasksize / self.workflow.forwardCP[taskNo]
        fastestFinishTime = (self.workflow.forwardCP[taskNo] - tasksize) / 1.4
        decompositeDeadline = self.workflow.DeadLine - self.currentTime - fastestFinishTime
        obs.append(decompositeDeadline)
        obs = np.array(obs)
        return obs

    def calcReward(self):
       # if self.currentTime >= self.workflow.DeadLine:
       #     reward = -80
       # else:
          # cost = self.getCurrentCost()
          # costLow = self.totalSize
          # costHigh = self.totalSize * 2.5
          # reward = ( (cost - costLow) / (costHigh - costLow) ) - 1
        reward = self.currentTime - self.workflow.DeadLine
        return  reward

    def getTaskToSchedule(self):
        tasksToSchedule = self.getNewTasks()
        if len(tasksToSchedule) != 0:
            taskNo = tasksToSchedule[0]
        else:
            taskNo = -1
        return taskNo

    def getNewTasks(self):
        pre_tasks = self.workflow.getNewTask()
        tasksToSchedule = list(set(pre_tasks) - set(self.runningTasks) - set(self.finishedTasks))
        if len(tasksToSchedule) > 0:
            tasksToSchedule.sort()
        return tasksToSchedule

    def scheduleTask(self, taskNo, vmType):
        if taskNo == -1:
            return 1, 'No available task to schedule!'

        if vmType == 0:
            vm = VM(speed=1, cost=1, type='small')
        if vmType == 1:
            vm = VM(speed=1.4, cost=1.7, type='medium')
        if vmType == 2:
            vm = VM(speed=1.8, cost=2.5, type='large')
        if vmType == 3:
            return 2, 'hold for current task'

        vm.assignTask(taskNo, self.workflow.taskSize[taskNo])
        self.resourcePool.append(vm)
        self.runningTasks.append(taskNo)
        return 4, 'schedule task t_'+str(taskNo)+' to vm_'+str(vmType)

    def setTaskFinished(self, taskNo):
        self.workflow.markAsFinished(taskNo)
        self.runningTasks.remove(taskNo)
        self.finishedTasks.append(taskNo)

    def isDone(self):
        if self.currentTime >= self.workflow.DeadLine:
            return True
        if len(self.finishedTasks) == self.workflow.taskCount:
            return True
        return False

    def reset(self, newWorkflow = False):
        if newWorkflow:
            self.workflow = Workflow(self.taskCount)
            self.workflowbak = copy.deepcopy(self.workflow)
        else:
            self.workflow = copy.deepcopy(self.workflowbak)

        self.runningTasks = []
        self.finishedTasks = []
        self.currentTime = 0
        self.resourcePool = []
        self.initVM()
        self.finishedSize = 0
        self.totalSize = sum(self.workflow.taskSize)
        self.totalCost = 0



