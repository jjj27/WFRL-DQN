from Env.Environment import Environment
import numpy as np

env = Environment(taskCount=10)

env.workflow.print()
cpt = env.workflow.CPTime

print('cptime:', cpt)
print('taskCP:', env.workflow.forwardCP)
print('DL: ', env.workflowbak.DeadLine)
print('\n\n')


s = env.getObservation()
while True:
    taskNo = env.getTaskToSchedule()
    a = np.random.randint(0,3)
    s_, r, done, succ = env.step(taskNo, vmType=a, s=s)

    if succ:
        print('task: ', taskNo)
        print('ob:', s)
        print('action: ', a, '\n')
    if done != 0:
        break
    s = s_
