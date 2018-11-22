from Env.Environment import Environment
from Env.VirtualMachine import VM
import numpy as np
import pickle


class ICPCP:
    def __init__(self, env):
        # ============  ENV start  ============
        self.env = env
        self.taskCount = env.taskCount
        self.exitNode  = self.taskCount


        # with open('env-10', 'rb') as file:
        #     self.env =pickle.load(file)
        #     self.env.workflow.print()
        # ============  ENV end  ============


        # ============  Var start  ============
        self.Assigned = np.zeros(self.taskCount)
        self.EST = np.zeros(self.taskCount)
        self.EFT = np.zeros(self.taskCount)
        self.LFT = np.zeros(self.taskCount)
        self.LFT[self.taskCount-1] = self.env.workflow.DeadLine

        self.MET = np.array(self.env.workflow.taskSize) / 1.8
        self.SS  = np.zeros(self.taskCount)
        self.AST = np.zeros(self.taskCount)
        self.getEST(self.taskCount-1)
        self.getLFT(0)
        # print('EST: ', self.EST)
        # print('EFT: ', self.EFT)
        # print('LFT: ', self.LFT)
        # print('Deadline: ', self.env.workflow.DeadLine)
        # ============  Var end  ============

    # ============  Init start  ============
    def getEST(self, taskNo):
        if taskNo == 0:
            self.EST[taskNo] == 0
            self.EFT[taskNo] = self.EST[taskNo] + self.MET[taskNo]
            return self.EST[taskNo]

        parents = self.env.workflow.DAG[:, taskNo]
        max = 0
        for j in range(self.taskCount):
            if parents[j] != 0:
                est = self.getEST(j) + self.MET[j]
                if est > max:
                    max = est
        self.EST[taskNo] = max
        self.EFT[taskNo] = self.EST[taskNo] + self.MET[taskNo]
        return self.EST[taskNo]

    def getLFT(self, taskNo):
        if self.LFT[taskNo] != 0:
            return self.LFT[taskNo]

        min = 999999999
        children = self.env.workflow.DAG[taskNo, :]
        for c in range(len(children)):
            if children[c] != 0:
                res = self.getLFT(c) - self.MET[c]
                if res < min:
                    min = res
                self.LFT[taskNo] = min
        return self.LFT[taskNo]


    # ============  Init end  ============






    def hasUnassignedParent(self, taskNo):
        # exit node
        if taskNo == self.exitNode:
            if self.Assigned[self.exitNode - 1] == 0:
                return True
            else:
                return False

        parents = self.env.workflow.DAG[:, taskNo]
        for i in range(len(parents)):
            if parents[i] != 0 and self.Assigned[i] == 0:
                return True
        return False

    def findCriticalParent(self, taskNo):
        # exit node
        if taskNo == self.exitNode:
            return self.exitNode - 1

        parents = self.env.workflow.DAG[:, taskNo]
        max = 0
        index = -1
        for i in range(len(parents)):
            if parents[i] != 0 and self.Assigned[i] == 0 and self.MET[i] > max:
                max = self.MET[i]
                index = i
        return index


    def chooseVM(self, PCP, speed):
        taskSize = self.env.workflow.taskSize
        startTime = self.getEST(PCP[0])

        for t in PCP:
            finishTime = startTime + (taskSize[t] / speed)
            startTime = finishTime
            if finishTime > self.LFT[t]:
                return False
        return True


    def AssignPath(self, PCP):
        vmtype = -1
        taskSize = self.env.workflow.taskSize

        if self.chooseVM(PCP, VM.small_speed):
            vmtype = 0
            speed = VM.small_speed
        elif self.chooseVM(PCP, VM.medium_speed):
            vmtype = 1
            speed = VM.medium_speed
        elif self.chooseVM(PCP, VM.large_speed):
            vmtype = 2
            speed = VM.large_speed
        elif self.chooseVM(PCP, VM.xlarge_speed):
            vmtype = 3
            speed = VM.xlarge_speed
        else:
            vmtype = 4
            speed = VM.xlarge_speed

        startTime = self.AST[PCP[0]]
        for t in PCP:
            self.MET[t] = taskSize[t] / speed
            self.SS[t] = vmtype
            self.AST[t] = startTime
            startTime = startTime + taskSize[t] / speed
            self.Assigned[t] = 1



    def AssignParents(self, taskNo):
        # print(taskNo, hasUnassignedParent(taskNo))
        while self.hasUnassignedParent(taskNo):
            PCP = []
            ti = taskNo

            while self.hasUnassignedParent(ti):
                ti = self.findCriticalParent(ti)
                PCP.insert(0, ti)

            self.AssignPath(PCP)

            for t in PCP:
                self.EST = np.zeros(self.taskCount)
                self.EFT = np.zeros(self.taskCount)
                self.getEST(self.taskCount-1)
                self.LFT = np.zeros(self.taskCount)
                self.LFT[self.taskCount-1] = self.env.workflow.DeadLine
                self.getLFT(0)
                self.AssignParents(t)


    def run(self):
        self.AssignParents(self.exitNode)


        step = 0
        costs = []
        while True:
            taskNos = self.env.getNewTasks()
            if len(taskNos) == 0:
                # self.env.spanTimeProcess()
                curCost = self.env.timeProcess()
                costs.append(curCost)
            else:
                for taskNo in taskNos:
                    vmType = self.SS[step]
                    step += 1
                    self.env.scheduleTask(taskNo, vmType)
                # self.env.spanTimeProcess()

                curCost = self.env.timeProcess()
                costs.append(curCost)
            done, r = self.env.isDone2()

            if done:
                # f = open("heatmap/ICPCP.txt", "a")
                # s = ''
                # for c in costs:
                #    s = s + str(c) + ' '
                # print(s, file=f)
                # f.close()

                print(self.env.currentTime, self.env.totalCost)

                if r < 0:
                    issucc = 'fail'
                    fail = True
                else:
                    issucc = 'meet deadline'
                    fail = False
                # print('Actions: ', self.SS)
                # print('DeadLine: ', self.env.workflow.DeadLine)
                # print('Time: ', self.env.currentTime, ' ', issucc)
                # print('Cost: ', self.env.totalCost)
                # print( )
                break
        types = []
        for i in range(5):
            types.append(np.count_nonzero(self.SS == i))
        
        cost = self.env.totalCost
        time = self.env.currentTime
        env = Environment(taskCount=self.taskCount)
        self.__init__(env)
        return fail, time, cost, types


if __name__ == '__main__':
    algo = 'ICPCP'
    wf = 'LIGO'
    alpha = 0.8
    dataset = './ScientificWorkflow/' + wf + '-' + str(alpha) + '-ENVs'
    
    with open(dataset, 'rb') as file:
        ENVs = pickle.load(file)
    done = False
    failNo = 0
    costs = []
    times = []
    VMtypes = []
    for i in range(len(ENVs)):
        env = ENVs[i]
        Pcp = ICPCP(env)
        fail, time, cost, types = Pcp.run()
        VMtypes.append(types)
        costs.append(cost)
        times.append(time)
        if fail:
            failNo += 1

    print()
    print('failNo: ', failNo)
    print('costMean: ', np.mean(costs))

    filename = "PlayOutput/" + wf + '-' + str(alpha) + '-' + algo + '.txt'
    f = open(filename, "w")
    f.truncate()
    f.close()

    f = open(filename, "a")
    s = ''

    for i in range(len(times)):
        print(times[i], costs[i], file=f)
    f.close()

    # AvgTypes = []
    # for i in range(5):
    #     curTs = 0
    #     l = len(VMtypes)
    #     for j in range(l):
    #         curTs += VMtypes[j][i]
    #     AvgTypes.append(curTs / l)
    # print(AvgTypes)
