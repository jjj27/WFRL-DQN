#!/usr/bin/python
# -*- coding: utf8 -*-

from Env.Workflow import Workflow
from Env.VirtualMachine import VM
import pickle
import copy
import numpy as np

class Environment:

    def __init__(self, taskCount=10, save = False, alpha = 0.5, workflow=None):
        self.taskCount = taskCount
        self.alpha = alpha
        if workflow is None:
            self.workflow  = Workflow(self.taskCount, self.alpha)
        else:
            self.workflow = copy.deepcopy(workflow)
            self.workflow.calcDeadline(self.alpha)
        self.workflowbak = copy.deepcopy(self.workflow)
        self.runningTasks  = []
        self.finishedTasks = []
        self.currentTime = 0
        self.resourcePool = []
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

    def getFinishRate(self):
        return self.finishedSize / self.totalSize

    def timeProcess(self):
        self.currentTime += 0.1
        toRemove = []
        curCost = 0
        for i in range(len(self.resourcePool)):
            finishSig, cost = self.resourcePool[i].timeProcess(self)
            curCost += cost
            self.totalCost += cost
            if finishSig:
                self.setTaskFinished(self.resourcePool[i].taskNo)
                toRemove.append(self.resourcePool[i])
        self.resourcePool = [e for e in self.resourcePool if e not in toRemove]
        return curCost

    def spanTimeProcess(self):
        min = 99999999
        for i in range(len(self.resourcePool)):
            if self.resourcePool[i].remainTime < min:
                min = self.resourcePool[i].remainTime

        if min == 99999999:
            return

        self.currentTime += min
        toRemove = []
        for i in range(len(self.resourcePool)):
            finishSig, cost = self.resourcePool[i].spanTimeProcess(self, min)
            self.totalCost += cost
            if finishSig:
                self.setTaskFinished(self.resourcePool[i].taskNo)
                toRemove.append(self.resourcePool[i])
        self.resourcePool = [e for e in self.resourcePool if e not in toRemove]

    def step(self, taskNo, vmType):
        self.scheduleTask(taskNo, vmType)
        self.timeProcess()
        done, reward = self.isDone()
        return done, reward

    def isDone(self):
        done = False
        reward = 0

        if self.currentTime >= self.workflow.DeadLine:
            # reward = -1
            reward = -0.01
            done = True

        # 正常完成
        if len(self.finishedTasks) == self.workflow.taskCount:
            fastFinishTime = self.workflow.CPTime / VM.xxlarge_speed
            finishTime = self.currentTime
            deadLine = self.workflow.DeadLine
            reward = (finishTime - fastFinishTime) / (deadLine - fastFinishTime)
            reward = reward * reward * reward
            done = True
        return done, reward

    def isDone2(self):
        done = False
        reward = 0


        # 正常完成
        if len(self.finishedTasks) == self.workflow.taskCount:
            if self.currentTime >= self.workflow.DeadLine:
                # reward = -1
                reward = -0.01
                done = True
            else:
                fastFinishTime = self.workflow.CPTime / VM.xxlarge_speed
                finishTime = self.currentTime
                deadLine = self.workflow.DeadLine
                reward = (finishTime - fastFinishTime) / (deadLine - fastFinishTime)
                reward = reward * reward * reward
                done = True
        return done, reward

    def getObservation(self, vmPerm = 1):
        obs = []
        taskNo = self.getTaskToSchedule()
        tasksize = self.workflow.taskSize[taskNo]
        obs.append(tasksize / VM.small_speed * vmPerm)
        obs.append(tasksize / VM.medium_speed * vmPerm)
        obs.append(tasksize / VM.large_speed * vmPerm)
        obs.append(tasksize / VM.xlarge_speed * vmPerm)
        obs.append(tasksize / VM.xxlarge_speed * vmPerm)

        fastestFinishTime = self.workflow.forwardCP[taskNo] - (tasksize / VM.xxlarge_speed)
        decompositeDeadline = self.workflow.DeadLine - self.currentTime - fastestFinishTime
        obs.append(decompositeDeadline)
        obs = np.array(obs)
        return obs

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
        vm = VM(vmType)
        vmPermformance = vm.assignTask(taskNo, self.workflow.taskSize[taskNo])
        self.resourcePool.append(vm)
        self.runningTasks.append(taskNo)
        return vmPermformance


    def setTaskFinished(self, taskNo):
        self.workflow.markAsFinished(taskNo)
        self.runningTasks.remove(taskNo)
        self.finishedTasks.append(taskNo)

    def reset(self, newWorkflow = False):
        if newWorkflow:
            self.workflow = Workflow(self.taskCount, self.alpha)
            self.workflowbak = copy.deepcopy(self.workflow)
        else:
            self.workflow = copy.deepcopy(self.workflowbak)

        self.runningTasks = []
        self.finishedTasks = []
        self.currentTime = 0
        self.resourcePool = []
        self.finishedSize = 0
        self.totalSize = sum(self.workflow.taskSize)
        self.totalCost = 0

    def reset2(self):
        self.workflow = Workflow(taskCount=self.taskCount, alpha=self.alpha, DAG=self.workflowbak.DAG)
        self.runningTasks = []
        self.finishedTasks = []
        self.currentTime = 0
        self.resourcePool = []
        self.finishedSize = 0
        self.totalSize = sum(self.workflow.taskSize)
        self.totalCost = 0


