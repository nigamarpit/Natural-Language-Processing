import time
import sys
import os
import copy
import random
from collections import Counter
from collections import defaultdict

class nbtrain(object):
	def __init__(self,path):
		self.path=path
		self.inputFiles=dict()
		self.feature_words=list()
		self.recursiveRead()
		self.weights=dict(Counter(self.feature_words))
		for key in list(self.weights.keys()):
			self.weights[key]=0
		self.avg_weights=self.weights.copy()
		#print(str(self.weights)+'\t'+str(self.avg_weights))
		self.alpha=0
		self.bias=0
		self.u=0
		self.beta=0
		self.count=0
		self.shuffleAndTrain()

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
		files=list(self.inputFiles.keys())
		for i in range(30):
			random.shuffle(files)
			self.train(files)

		self.beta=self.bias-(1.0/self.count)*self.beta
		for x in self.avg_weights:
			self.avg_weights[x]=self.weights[x]-(1.0/self.count)*self.avg_weights[x]

		f=open('per_model.txt','w',encoding='latin1')
		f.write(str([self.beta,self.avg_weights]))
		f.close()

	def train(self,files):
		for file in files:
			if self.inputFiles[file][0]=='spam':
				y=1
			else:
				y=-1
			self.computations(self.inputFiles[file][1],y)

	def computations(self,x,y):
		self.count+=1
		alpha=0
		for word in x:
			alpha+=self.weights[word]
		alpha+=self.bias
		if (y*alpha)<=0:
			for word in x:
				self.weights[word]+=y
				self.avg_weights[word]+=y*self.count
			self.bias+=y
			self.beta+=y*self.count

start_time = time.time()
nbtrain(sys.argv[1])
print("Train time: %s "%(time.time() - start_time))
#python avg_per_learn.py "C:\Users\Xenon\Documents\GitHub\Natural-Language-Processing\Perceptron\Spam or Ham\train"
#python avg_per_learn.py "C:\Users\Xenon\Documents\GitHub\Natural-Language-Processing\Perceptron\Data\train"