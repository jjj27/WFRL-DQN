from Env.Environment import Environment, VM
import pickle
from pyswarm import pso
import numpy as np




class Pso():
	def __init__(self, env):
		self.env = env
		self.taskSize = self.env.workflow.taskSize
		self.taskCount = self.env.taskCount

	def wf(self, x, *args):
		taskSize = args
		cost = 0
		for i in range(len(x)):
			vmtype = int(x[i])
			size = taskSize[i]
			if vmtype == 0:
				cost += size / VM.small_speed * VM.small_cost
			elif vmtype == 1:
				cost += size / VM.medium_speed * VM.medium_cost
			elif vmtype == 2:
				cost += size / VM.large_speed * VM.large_cost
			elif vmtype == 3:
				cost += size / VM.xlarge_speed * VM.xlarge_cost
			elif vmtype == 4:
				cost += size / VM.xxlarge_speed * VM.xxlarge_cost
		return cost

	def costReplay(self, x, taskSize):
		self.env.reset(newWorkflow=False)
		cost = 0
		for i in range(len(x)):
			vmtype = int(x[i])
			size = taskSize[i]
			if vmtype == 0:
				cost += size / VM.small_speed * VM.small_cost
			elif vmtype == 1:
				cost += size / VM.medium_speed * VM.medium_cost
			elif vmtype == 2:
				cost += size / VM.large_speed * VM.large_cost
			elif vmtype == 3:
				cost += size / VM.xlarge_speed * VM.xlarge_cost
			elif vmtype == 4:
				cost += size / VM.xxlarge_speed * VM.xxlarge_cost
		return cost

	def timeReplay(self, x, taskSize):
		self.env.reset(newWorkflow=False)
		tmpSize = taskSize
		for i in range(len(x)):
			vmtype = int(x[i])
			size = taskSize[i]
			if vmtype == 0:
				tmpSize[i] = size / VM.small_speed
			elif vmtype == 1:
				tmpSize[i] = size / VM.medium_speed
			elif vmtype == 2:
				tmpSize[i] = size / VM.large_speed
			elif vmtype == 3:
				tmpSize[i] = size / VM.xlarge_speed
			elif vmtype == 4:
				tmpSize[i] = size / VM.xxlarge_speed
		self.env.workflow.taskSize = tmpSize
		self.env.workflow.CP = np.zeros(self.taskCount, dtype=float)
		executionTime = self.env.workflow.getCP(self.taskCount - 1)
		self.env.workflow.taskSize = taskSize
		return executionTime


	def con(self, x, *args):
		# taskSize = args
		taskSize = self.env.workflow.taskSize
		taskTimes = []
		for i in range(len(x)):
			vmtype = int(x[i])
			size = taskSize[i] * 1.12

			if vmtype == 0:
				taskTimes.append(size / VM.small_speed)
			elif vmtype == 1:
				taskTimes.append(size / VM.medium_speed)
			elif vmtype == 2:
				taskTimes.append(size / VM.large_speed)
			elif vmtype == 3:
				taskTimes.append(size / VM.xlarge_speed)
			elif vmtype == 4:
				taskTimes.append(size / VM.xxlarge_speed)

		self.env.workflow.taskSize = taskTimes
		self.env.workflow.CP = np.zeros(self.env.workflow.taskCount, dtype=float)
		totalExecutionTime = self.env.workflow.getCP(self.env.workflow.taskCount - 1)
		self.env.reset(newWorkflow=False)
		return self.env.workflow.DeadLine - totalExecutionTime

	def judge(self, x):
		self.env.reset(newWorkflow=False)
		#self.env.workflow.DeadLine += 1
		while True:
			taskNos = self.env.getNewTasks()
			if len(taskNos) == 0:
				self.env.spanTimeProcess()
			else:
				for taskNo in taskNos:
					vmType = x[taskNo]
					self.env.scheduleTask(taskNo, vmType)
				self.env.timeProcess()
			done, reward = self.env.isDone2()
			if done:
				break

		return reward, self.env.currentTime, self.env.totalCost

	def run(self):
		lb = []
		ub = []

		for i in range(self.taskCount):
			lb.append(0)
			ub.append(4)

		args = (self.taskSize)

		xopt, fopt = pso(self.wf, lb, ub, f_ieqcons=self.con, args=args, maxiter=100)

		for i in range(len(xopt)):
			xopt[i] = int(xopt[i])
		reward, time, cost = self.judge(xopt)
		return reward, time, cost

			# print()
			# print('============ PLAN ============')
			# print("Actions: ", xopt)
			# print('Cost: ', fopt)
			# print('CostReplay: ', costReplay(xopt, taskSize))
			# print('TimeReplay: ', timeReplay(xopt, taskSize))
			# print("DeadLine: ", env.workflow.DeadLine)
			# print()
			#
			# print('============ Actual ============')
			# reward, time, cost = judge(xopt)
			# print("Reward: ", reward)
			# print("Time: ", time)
			# print("Cost: ", cost)


if __name__ == '__main__':
	with open('./ScientificWorkflow/Epig-0.4-ENVs', 'rb') as file:
		ENVs = pickle.load(file)
	times = []
	costs = []
	fail = 0
	for i in range(len(ENVs)):
		p = Pso(ENVs[i])
		reward, time, cost = p.run()
		times.append(time)
		costs.append(cost)
		if reward < 0:
			fail += 1

	print()
	print("fail: ", fail)
	print()
	for i in range(len(times)):
		print(times[i], costs[i])