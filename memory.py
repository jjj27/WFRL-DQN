import random
import numpy as np

class MemoryReplay(object):

	def __init__(self,
				 max_size=10000,
				 bs=64,
				 im_size=84,
				 stack=4):     # stack ？

		self.s = np.zeros((max_size, 6), dtype=np.float32) # states
		self.r = np.zeros(max_size, dtype=np.float32)                              # rewards
		self.a = np.zeros(max_size, dtype=np.int32)                                # actions
		#self.ss = np.zeros_like(self.s)
		self.done = np.array([True]*max_size)                                      # game state?

		self.max_size = max_size
		self.bs = bs
		self._cursor = None
		self.total_idx = list(range(self.max_size))


	def put(self, sras):
		# print(sras)
		if self._cursor == (self.max_size-1) or self._cursor is None :
			self._cursor = 0
		else:
			self._cursor += 1

		self.s[self._cursor] = sras[0]
		self.a[self._cursor] = sras[1]
		self.r[self._cursor] = sras[2]
		#self.ss[self._cursor] = sras[3]
		self.done[self._cursor] = sras[3]


	def batch(self):

		sample_idx = random.sample(self.total_idx, self.bs)
		s = self.s[sample_idx]          # state 只要前四个？ 前四个通道都要
		a = self.a[sample_idx]
		a = a[:, np.newaxis]
		r = self.r[sample_idx]
		r = r[:, np.newaxis]
		#ss = self.ss[sample_idx]
		# ss = self.s[sample_idx, 1:]		  # 不要第一个？     只要后三个通道？
		ss = self.s[sample_idx]
		done = self.done[sample_idx]
		done = done[:, np.newaxis]

		return s, a, r, ss, done
