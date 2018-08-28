#!/usr/bin/python
# -*- coding: UTF-8 -*-

from xml.dom.minidom import parse
import xml.dom.minidom
import numpy as np


class XMLtoDAG():

	def __init__(self, file, taskCount):
		self.xmlFile = file
		self.taskCount = taskCount
		self.DAG = np.zeros((self.taskCount, self.taskCount), dtype=int)

	def getDAG(self):

		# 使用minidom解析器打开 XML 文档
		DOMTree = xml.dom.minidom.parse(self.xmlFile)
		collection = DOMTree.documentElement
		childrens = collection.getElementsByTagName("child")

		for child in childrens:
			child_id = child.getAttribute('ref')
			child_id = int(child_id[2:])
			# print('Child: ', child_id)
			parents = child.getElementsByTagName('parent')
			for parent in parents:
				parent_id = parent.getAttribute('ref')
				parent_id = int(parent_id[2:])
				# print(parent_id)
				self.DAG[parent_id, child_id] = 1
		return self.DAG



if __name__ == '__main__':
	dag = XMLtoDAG("CyberShake_30.xml", taskCount=30).getDAG()
	print(dag)
	for i in range(30):
		for j in range(30):
			if dag[i,j] != 0:
				print(i, ' -> ', j)