import time
import sys
import os
import copy
from collections import Counter

class nbtrain(object):
	def __init__(self,path):
		try:
			# TASK 1
			self.path=path
			self.hamWordList=list()
			self.spamWordList=list()
			self.wordList=list()
			self.hamDict=dict()
			self.spamDict=dict()
			self.wordDict=dict()
			self.spamCount=0
			self.hamCount=0 
			self.recursiveRead()
			self.writeModel()
			## TASK 2
			n=self.hamCount+self.spamCount
			self.n=(n/20,n/20+1)[n%20!=0]
			self.task2()
			self.writeModel2()
			### TASK 3
			self.task3()
			#self.writeModel3()
		except:
			print('Unexpected Error Encountered')

	def recursiveRead(self):
		for subdir, dirs, files in os.walk(self.path):
			if subdir.endswith('spam'):
				for file in files:
					if file.endswith('.txt'):
						f=open(os.path.join(subdir, file),'r',encoding='latin1')
						self.spamWordList.extend(f.read().split())
						f.close()
						self.spamCount+=1
			if subdir.endswith('ham'):
				for file in files:			
					if file.endswith('.txt'):
						f=open(os.path.join(subdir, file),'r',encoding='latin1')
						self.hamWordList.extend(f.read().split())
						f.close()
						self.hamCount+=1

	def writeModel(self):
		self.hamDict=dict(Counter(self.hamWordList))
		self.spamDict=dict(Counter(self.spamWordList))
		self.wordList=self.hamWordList.copy()
		self.wordList.extend(self.spamWordList)
		self.wordDict=dict(Counter(self.wordList))
		f=open('nbmodel.txt','w+',encoding='latin1')
		l=[self.hamCount,self.spamCount,len(self.hamWordList),len(self.spamWordList),len(self.wordDict),self.hamDict,self.spamDict]
		f.write(str(l))
		f.close()

	def task2(self):
		n=int(self.n)
		m=int(self.n)
		self.spamWordList2=list()
		self.hamWordList2=list()
		for subdir, dirs, files in os.walk(self.path):
			if subdir.endswith('spam') and n>0:
				for file in files:
					if file.endswith('.txt') and n>0:
						#print(n,os.path.join(subdir, file))
						f=open(os.path.join(subdir, file),'r',encoding='latin1')
						self.spamWordList2.extend(f.read().split())
						f.close()
						n-=1
					else:
						break
			if subdir.endswith('ham') and m>0:
				for file in files:			
					if file.endswith('.txt') and m>0:
						#print(m,os.path.join(subdir, file))
						f=open(os.path.join(subdir, file),'r',encoding='latin1')
						self.hamWordList2.extend(f.read().split())
						f.close()
						m-=1
					else:
						break

	def writeModel2(self):
		self.hamDict2=dict(Counter(self.hamWordList2))
		self.spamDict2=dict(Counter(self.spamWordList2))
		self.wordList2=self.hamWordList2.copy()
		self.wordList2.extend(self.spamWordList2)
		self.wordDict2=dict(Counter(self.wordList2))
		f=open('nbmodel2.txt','w+',encoding='latin1')
		l=[int(self.n),int(self.n),len(self.hamWordList2),len(self.spamWordList2),len(self.wordDict2),self.hamDict2,self.spamDict2]
		f.write(str(l))
		f.close()

	def task3(self):
		hamDict3=self.hamDict.copy()
		spamDict3=self.spamDict.copy()

		### REMOVE COMMON WORDS: STOP WORDS
		stopWords=['a','an','and','are','as','at','be','by','for','from','has','he','in','is','it','its','of','on','that','the','to','was','were','will','with']
		for x in stopWords:
			try:
				del hamDict3[x]
			except:
				pass
			try:	
				del spamDict3[x]
			except:
				pass

		### HIGHER FREQUENCY WORDS
		for x in list(hamDict3.keys()):
			if hamDict3[x]==1:
				del hamDict3[x]
		for x in list(spamDict3.keys()):
			if spamDict3[x]==1:
				del spamDict3[x]

		wordDict=set(hamDict3.keys())|set(spamDict3.keys())
		l=[self.hamCount,self.spamCount,sum(list(hamDict3.values())),sum(list(spamDict3.values())),len(wordDict),hamDict3,spamDict3]
		f=open('nbmodel3.txt','w+',encoding='latin1')
		f.write(str(l))
		f.close()

start_time = time.time()
#print(start_time)
nbtrain(sys.argv[1])
print("Train time: %s "%(time.time() - start_time))
#python nblearn.py "C:\Users\Xenon\Documents\GitHub\Natural-Language-Processing\Naive Bayes\Spam or Ham\train"