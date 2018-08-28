#!/usr/bin/python
# -*- coding: utf8 -*-

import numpy as np
import random
from Env.VirtualMachine import VM
import copy


class Workflow:

    def __init__(self, taskCount = 10, alpha = 0.5, DAG = None):
        self.alpha = alpha
        self.taskCount = taskCount
        if DAG is None:
            self.DAG = np.zeros((taskCount, taskCount), dtype=int)
            self.randomGenerate()
        else:
            self.DAG = copy.deepcopy(DAG)
        self.taskSize = self.generateTaskSizeRandom()
        self.taskTime = np.array(self.taskSize) / VM.xxlarge_speed

        self.CP = np.zeros(taskCount, dtype=float)
        # self.taskCP = np.zeros(taskCount, dtype=int)
        self.forwardCP = np.zeros(taskCount, dtype=float)
        self.CPTime = self.getCP(self.taskCount-1) # loose
        self.getForwardCP(0)                       # tight
        self.DeadLine = (self.CPTime / VM.xxlarge_speed) + (self.CPTime - self.CPTime / VM.xxlarge_speed) * alpha
        # self.DeadLine = self.CPTime * 1

        # self.taskCPs = []
        # for i in range(taskCount):
        #     self.taskCPs.append([])
        # for i in range(taskCount-1):
        #     next = self.taskCP[i]
        #     self.taskCPs[i].append(next)
        #     while next != taskCount-1:
        #         next = self.taskCP[next]
        #         self.taskCPs[i].append(next)

    def calcDeadline(self, alpha):
        self.DeadLine = (self.CPTime / VM.xxlarge_speed) + (self.CPTime - self.CPTime / VM.xxlarge_speed) * alpha

    # CPTime: end node -> start node
    def getCP(self, taskNo):
        if taskNo == 0:
            self.CP[taskNo] = self.taskSize[0]
            return self.CP[taskNo]
        if self.CP[taskNo] != 0:
            return self.CP[taskNo]

        pre = self.DAG[:,taskNo]
        cp  = 0
        for i in range(len(pre)):
            preTaskNo = i;
            if pre[i] != 0:
                preCP = self.getCP(preTaskNo)
                if preCP > cp:
                    cp = preCP

        self.CP[taskNo] = self.taskSize[taskNo] + cp;
        return self.CP[taskNo]

    def getForwardCP(self, taskNo):
        if taskNo == self.taskCount - 1 : # end node
            self.forwardCP[taskNo] = self.taskTime[taskNo]
            return self.forwardCP[taskNo]
        if self.forwardCP[taskNo] != 0:
            return self.forwardCP[taskNo]

        pre = self.DAG[taskNo, :]
        cp  = 0
        index = 0
        for i in range(len(pre)):
            preTaskNo = i
            if pre[i] != 0:
                preCP = self.getForwardCP(preTaskNo)
                if preCP > cp:
                    cp = preCP
                    index = i

        # if cp != 0:
        #     self.taskCP[taskNo] = index

        self.forwardCP[taskNo] = self.taskTime[taskNo] + cp
        return self.forwardCP[taskNo]


    def markAsFinished(self, taskNo):
        self.DAG[taskNo, :] = 0

    def getNewTask(self):
        newTasks = []
        for i in range(self.taskCount):
            # 判断一个任务是否可以开始（是否有前驱节点）
            flag = True
            for e in self.DAG[:,i]:
                if e != 0:
                    flag = False
            if flag:
                newTasks.append(i)

        return newTasks

    def randomGenerate(self):
        for i in range(0, self.taskCount-1):
            edge = random.randint(i + 1, self.taskCount - 1)
            self.DAG[i, edge] = 1


        for i in range(1, self.taskCount-1):
            flag = True
            for e in self.DAG[:,i]:
                if e != 0:
                    flag = False
                    break

            if flag:
                edge = random.randint(0, i - 1)
                self.DAG[edge, i] = 1

        for i in range(0, self.taskCount-1):
            for j in range(i+1, self.taskCount-1):
                if random.randint(0, 10) > 99:
                    self.DAG[i,j] = 1

    def print(self):
        print("DAG: ")
        print(self.DAG)
        print("TaskSize: ")
        print(self.taskSize)
        print("DeadLine: ", self.DeadLine)
        print()

    def generateTaskSizeRandom(self):
        tasksize = []
        for i in range(self.taskCount):
            if random.randint(0, 10) > 5:
                tasksize.append(random.randint(4, 10))
            else:
                tasksize.append(random.randint(14, 16))
        return tasksize


if __name__ == '__main__':
    w = Workflow()
    w.print()
    print(w.getCP(w.taskCount-1))



