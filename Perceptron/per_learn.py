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
		self.features=dict(Counter(self.feature_words))
		for key in list(self.features.keys()):
			self.features[key]=0

		self.y_label=1
		self.y_label=-1
		self.alpha=0
		self.bias=0
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
		keys=list(self.inputFiles.keys())
		self.c=0
		for i in range(20):
			print(str(i)+'\t'+str(self.c))
			random.shuffle(keys)
			self.train(keys)

		f=open('test.txt','w',encoding='latin1')
		f.write(str([self.bias,self.features]))
		f.close()

	def train(self,keys):
		#print(self.inputFiles[keys[0]][0]+str(self.inputFiles[keys[0]][1]))
		for key in keys:
			#print(key)
			if self.inputFiles[key][0]=='spam':
				y=1
			else:
				y=-1
			self.computations(self.inputFiles[key][1],y)

	def computations(self,x,y):
		self.c+=1
		#input(y)
		#print(x)
		alpha=0
		for word in x:
			alpha+=self.features[word]
		alpha+=self.bias
		if (y*alpha)<=0:
			for word in x:
				self.features[word]+=y
			self.bias+=y
		'''
		f=open('test.txt','w',encoding='latin1')
		f.write(str(self.features))
		f.close()
		input(self.bias)
		'''



start_time = time.time()
#print(start_time)
nbtrain(sys.argv[1])
print("Train time: %s "%(time.time() - start_time))
#python per_learn.py "C:\Users\Xenon\Documents\GitHub\Natural-Language-Processing\Perceptron\Spam or Ham\train"