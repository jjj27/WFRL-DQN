#!/usr/bin/python
# -*- coding: utf8 -*-

import numpy as np
import time

class VM:

    small_speed   = 1
    small_cost    = 1

    medium_speed  = 1.87
    medium_cost   = 2

    large_speed   = 3.43
    large_cost    = 4

    xlarge_speed  = 6
    xlarge_cost  = 8

    xxlarge_speed = 11.42
    xxlarge_cost = 16

    average_speed = np.mean([small_speed, medium_speed, large_speed, xlarge_speed, xxlarge_speed])
    average_cost  = np.mean([small_cost, medium_cost, large_cost, xlarge_cost, xxlarge_cost])


    def __init__(self, type=0, timeStep = 0.1):
        self.taskNo     = -1
        self.taskSize   = -1
        self.remainTime = -1
        self.totalCost  = 0
        self.timeStep   = timeStep
        self.type       = type
        if type == 1:     # medium
            self.speed = VM.medium_speed
            self.cost  = VM.medium_cost
        elif type == 2:   # large
            self.speed = VM.large_speed
            self.cost  = VM.large_cost
        elif type == 3:   # large
            self.speed = VM.xlarge_speed
            self.cost  = VM.xlarge_cost
        elif type == 4:   # large
            self.speed = VM.xxlarge_speed
            self.cost  = VM.xxlarge_cost
        else:             # small
            self.speed = VM.small_speed
            self.cost  = VM.small_cost

    def assignTask(self, taskNo, taskSize):
        self.taskNo = taskNo
        self.taskSize = taskSize / self.speed
        vmPermformance = self.getFluctuationFactor()
        self.remainTime = taskSize / self.speed * vmPermformance
        return vmPermformance

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

    def spanTimeProcess(self, env, time):
        finishSingal = False
        if self.remainTime > 0:
            self.remainTime -= time
            cost = (self.cost * time)
            self.totalCost += cost
            env.finishedSize += self.speed * time
            if self.remainTime <= 0:
                finishSingal = True
        return finishSingal, cost

    def getFluctuationFactor(self):
        mu = 0.12
        sigma = 0.10
        t = time.time()
        t = int(round(t - int(t), 6) * 1e6)
        np.random.seed(t)
        s = np.random.normal(mu, sigma)
        return 1+s
        #return 1