#!/usr/bin/python
# -*- coding: utf8 -*-

class VM:
    def __init__(self, speed = 1, cost = 1, timeStep = 0.1, type='default'):
        self.taskNo     = -1
        self.taskSize   = -1
        self.remainTime = -1
        self.speed      = speed
        self.cost       = cost
        self.totalCost  = 0
        self.timeStep   = timeStep
        self.type       = type

    def assignTask(self, taskNo, taskSize):
        self.taskNo = taskNo
        self.taskSize = taskSize / self.speed
        self.remainTime = taskSize / self.speed

    def reset(self):
        self.taskNo     = -1
        self.taskSize   = -1
        self.remainTime = -1

    def timeProcess(self, env):
        finishSingal = False
        if self.remainTime > 0:
            self.remainTime -= self.timeStep
            cost = (self.cost * self.timeStep)
            self.totalCost  += cost
            env.finishedSize += self.speed * self.timeStep
            if self.remainTime <= 0:
                finishSingal = True
        return finishSingal, cost