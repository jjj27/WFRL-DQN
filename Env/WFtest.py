from Env.Environment import Environment
import numpy as np
import time

env = Environment(taskCount=10, alpha=0.5)
env.workflow.print()

cpt = env.workflow.CPTime

print('cptime:', cpt)
print('forwardCP:', env.workflow.forwardCP)
print('DL: ', env.workflowbak.DeadLine)
print('\n\n')


t = time.time()
actions = []
while True:

    taskNos = env.getNewTasks()
    if len(taskNos) == 0:
        env.spanTimeProcess()
        done, reward = env.isDone()
        if done:
            ob = env.getObservation()

            print('Actions: ', actions, 'Reward: ', reward)
            print('DeadLine:', env.workflow.DeadLine, ' Makespan: ', env.currentTime)
            print('Cost: ', env.totalCost)
            break
    else:
        for taskNo in taskNos:
            ob = env.getObservation()

            # vt = np.random.randint(0, 3)
            # print(ob)
            # vt = int(input('taskNo: ' + str(taskNo) + ' vmType:'))
            if ob[0] < ob[5]:
                vt = 0
            elif ob[1] < ob[5]:
                vt = 1
            elif ob[2] < ob[5]:
                vt = 2
            elif ob[3] < ob[5]:
                vt = 3
            elif ob[4] < ob[5]:
                vt = 4
            else:
                vt = 5
            actions.append(vt)

            done, reward = env.step(taskNo, vmType=vt)
            # print(ob, reward, done)


print(time.time() - t)