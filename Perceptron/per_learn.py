import time
import sys
import os
import copy
import random
from collections import Counter
import traceback

class perTrain(object):
	def __init__(self,path):
		try:
			self.path=path
			self.inputFiles=dict()
			self.feature_words=list()
			self.recursiveRead()
			self.weights=dict(Counter(self.feature_words))
			for key in list(self.weights.keys()):
				self.weights[key]=0
			self.alpha=0
			self.bias=0
			self.shuffleAndTrain()

		except Exception as e:
			traceback.print_exc()
			print('Unexpected Error Encountered')

	def recursiveRead(self):
		for subdir, dirs, files in os.walk(self.path):
			if subdir.endswith('spam'):
				for file in files:
					if file.endswith('.txt'):
						f=open(os.path.join(subdir, file),'r',encoding='latin1')
						l=f.read().split()
						self.inputFiles[str(os.path.join(subdir, file))]=['spam',l]
						self.feature_words.extend(l)
						f.close()

			if subdir.endswith('ham'):
				for file in files:			
					if file.endswith('.txt'):
						f=open(os.path.join(subdir, file),'r',encoding='latin1')
						l=f.read().split()
						self.inputFiles[str(os.path.join(subdir, file))]=['ham',l]
						self.feature_words.extend(l)
						f.close()

	def shuffleAndTrain(self):
		keys=list(self.inputFiles.keys())
		for i in range(20):
			random.shuffle(keys)
			self.train(keys)

		f=open('per_model.txt','w',encoding='latin1')
		f.write(str([self.bias,self.weights]))
		f.close()

	def train(self,keys):
		for key in keys:
			if self.inputFiles[key][0]=='spam':
				y=1
			else:
				y=-1
			self.computations(self.inputFiles[key][1],y)

	def computations(self,x,y):
		alpha=0
		for word in x:
			alpha+=self.weights[word]
		alpha+=self.bias
		if (y*alpha)<=0:
			for word in x:
				self.weights[word]+=y
			self.bias+=y

#start_time = time.time()
perTrain(sys.argv[1])
#print("Train time: %s "%(time.time() - start_time))
#python per_learn.py "C:\Users\Xenon\Documents\GitHub\Natural-Language-Processing\Perceptron\Spam or Ham\train"
#python3 per_learn.py "/mnt/c/Users/Xenon/Documents/GitHub/Natural-Language-Processing/Perceptron/Spam or Ham/train"