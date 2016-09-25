import time
import sys
import os
import math
from collections import Counter
class nbclassify(object):
	def __init__(self,path):
		try:
			# TASK 1
			self.path=path
			self.res=list()
			f=open('nbmodel.txt','r',encoding='latin1')
			l=eval(f.read())
			f.close()
			self.P_ham=math.log(l[0]/(l[0]+l[1]))
			self.P_spam=math.log(l[1]/(l[0]+l[1]))
			self.hamCount=l[0]
			self.spamCount=l[1]
			self.hamWordCount=l[2]
			self.spamWordCount=l[3]
			self.v=l[4]
			self.hamDict=l[5]
			self.spamDict=l[6]
			self.recursiveRead()
			self.writeFile()
			## TASK 2
			self.task2()
			### TASK 3
			self.task3()
		except:
			print('Unexpected Error Encountered')

	def recursiveRead(self):
		for subdir, dirs, files in os.walk(self.path):
			for file in files:
				if file.endswith('.txt'):
					self.res.append(self.fileTest(os.path.join(subdir, file)))

	def fileTest(self,file):		
		p_ham=0
		p_spam=0
		f=open(file,'r',encoding='latin1')
		d=f.read().split()
		f.close()
		for x in d:
			if self.hamDict.get(x,0)==0 and self.spamDict.get(x,0)==0:
				continue
			p_ham+=math.log((self.hamDict.get(x,0)+1)/(self.hamWordCount+self.v))
			p_spam+=math.log((self.spamDict.get(x,0)+1)/(self.spamWordCount+self.v))
		if (p_ham+self.P_ham)>(p_spam+self.P_spam):
			return ('ham',file)
		return ('spam',file)

	def writeFile(self):
		f=open('nboutput.txt','w+')
		for x in self.res:
			f.write(str(x[0])+' '+str(x[1])+'\n')
		f.close()

	def task2(self):
		f=open('nbmodel2.txt','r',encoding='latin1')
		l2=eval(f.read())
		f.close()
		self.P_ham2=math.log(l2[0]/(l2[0]+l2[1]))
		self.P_spam2=math.log(l2[1]/(l2[0]+l2[1]))
		self.hamCount2=l2[0]
		self.spamCount2=l2[1]
		self.hamWordCount2=l2[2]
		self.spamWordCount2=l2[3]
		self.v2=l2[4]
		self.hamDict2=l2[5]
		self.spamDict2=l2[6]
		self.recursiveRead2()

	def recursiveRead2(self):
		prediction=list()
		actual=list()
		correctSpam=0
		correctHam=0
		for subdir, dirs, files in os.walk(self.path):
			if subdir.endswith('spam'):
				for file in files:
					if file.endswith('.txt'):
						a=self.fileTest2(os.path.join(subdir, file))
						b='spam'
						if(a==b):
							correctSpam+=1
						prediction.append(a)
						actual.append(b)

						
			if subdir.endswith('ham'):
				for file in files:			
					if file.endswith('.txt'):
						a=self.fileTest2(os.path.join(subdir, file))
						b='ham'
						if(a==b):
							correctHam+=1
						prediction.append(a)
						actual.append(b)
		self.writeOutput(prediction,actual,correctHam,correctSpam,'Task2Output.txt')

	def fileTest2(self,file):		
		p_ham=0
		p_spam=0
		f=open(file,'r',encoding='latin1')
		d=f.read().split()
		for x in d:
			if self.hamDict2.get(x,0)==0 and self.spamDict2.get(x,0)==0:
				continue
			p_ham+=math.log((self.hamDict2.get(x,0)+1)/(self.hamWordCount2+self.v))
			p_spam+=math.log((self.spamDict2.get(x,0)+1)/(self.spamWordCount2+self.v))
		if (p_ham+self.P_ham2)>(p_spam+self.P_spam2):
			return 'ham'
		return 'spam'

	def task3(self):
		f=open('nbmodel3.txt','r',encoding='latin1')
		l3=eval(f.read())
		f.close()
		self.P_ham3=math.log(l3[0]/(l3[0]+l3[1]))
		self.P_spam3=math.log(l3[1]/(l3[0]+l3[1]))
		self.hamCount3=l3[0]
		self.spamCount3=l3[1]
		self.hamWordCount3=l3[2]
		self.spamWordCount3=l3[3]
		self.v3=l3[4]
		self.hamDict3=l3[5]
		self.spamDict3=l3[6]
		self.recursiveRead3()

	def recursiveRead3(self):
		prediction=list()
		actual=list()
		correctSpam=0
		correctHam=0
		for subdir, dirs, files in os.walk(self.path):
			if subdir.endswith('spam'):
				for file in files:
					if file.endswith('.txt'):
						a=self.fileTest3(os.path.join(subdir, file))
						b='spam'
						if(a==b):
							correctSpam+=1
						prediction.append(a)
						actual.append(b)
						
			if subdir.endswith('ham'):
				for file in files:			
					if file.endswith('.txt'):
						a=self.fileTest3(os.path.join(subdir, file))
						b='ham'
						if(a==b):
							correctHam+=1
						prediction.append(a)
						actual.append(b)
		self.writeOutput(prediction,actual,correctHam,correctSpam,'Task3Output.txt')

	def fileTest3(self,file):		
		p_ham=0
		p_spam=0
		f=open(file,'r',encoding='latin1')
		d=f.read().split()
		for x in d:
			if self.hamDict3.get(x,0)==0 and self.spamDict3.get(x,0)==0:
				continue
			p_ham+=math.log((self.hamDict3.get(x,0)+1)/(self.hamWordCount3+self.v))
			p_spam+=math.log((self.spamDict3.get(x,0)+1)/(self.spamWordCount3+self.v))
		if (p_ham+self.P_ham3)>(p_spam+self.P_spam3):
			return 'ham'
		return 'spam'

	def writeOutput(self,prediction,actual,correctHam,correctSpam,fileName):
		p=Counter(prediction)
		a=Counter(actual)
		precision_ham=correctHam/dict(p)['ham']
		precision_spam=correctSpam/dict(p)['spam']
		recall_ham=correctHam/dict(a)['ham']
		recall_spam=correctSpam/dict(a)['spam']
		f1_ham=(2*precision_ham*recall_ham)/(precision_ham+recall_ham)
		f1_spam=(2*precision_spam*recall_spam)/(precision_spam+recall_spam)
		res=list()
		res.append('--'+fileName.split('.')[0]+'--\n')
		res.append('spam precision: '+str(round(precision_spam,2))+'\n')
		res.append('spam recall: '+str(round(recall_spam,2))+'\n')
		res.append('spam F1 score: '+str(round(f1_spam,2))+'\n')
		res.append('ham precision: '+str(round(precision_ham,2))+'\n')
		res.append('ham recall: '+str(round(recall_ham,2))+'\n')
		res.append('ham F1 score: '+str(round(f1_ham,2))+'\n')
		f=open(fileName,'w+')
		f.write(''.join(res))
		f.close()
		print(''.join(res))

start_time = time.time()
#print(start_time)
nbclassify(sys.argv[1])
print("Classify Time: %s "%(time.time() - start_time))
#python nbclassify.py "C:\Users\Xenon\Desktop\Work\csci544\Spam or Ham\dev"