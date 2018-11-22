from Env.Workflow import Workflow
from ScientificWorkflow.XMLProcess import XMLtoDAG
import pickle


taskCount = 30
alpha = 0.2
dag = XMLtoDAG("LIGO_30.xml", taskCount=taskCount).getDAG()

wfs = []
for i in range(100):
	wf = Workflow(taskCount=taskCount, alpha=alpha, DAG=dag)
	wfs.append(wf)

dbfile = open('LIGO-Origin', 'wb')
pickle.dump(wfs, dbfile)
dbfile.close()


