import pickle
import numpy as np

with open('Epig-0.2-ENVs', 'rb') as file:
	ENVs = pickle.load(file)

deadlines = []
for e in ENVs:
	deadlines.append(e.workflow.DeadLine)
	print(e.workflow.DeadLine)

print()
print(np.mean(deadlines))
