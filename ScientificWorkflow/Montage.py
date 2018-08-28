from Env.Environment import Environment
from Env.Workflow import Workflow
import numpy as np

class Montate(Workflow):

	def __init__(self, alpha = 0.4):
		super(Montate, self).__init__(taskCount = 100, alpha = alpha)
		self.DAG = np.zeros((self.taskCount, self.taskCount), dtype=int)

mm = Montate(alpha=0.8)
print(mm.DAG)