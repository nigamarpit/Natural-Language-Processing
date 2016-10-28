import time
import sys
import os
import math
from collections import Counter

class perClassify(object):
	def __init__(self,path,outputFile):
		try:
			self.outputFile=outputFile
			self.path=path
			f=open('per_model.txt','r',encoding='latin1')
			l=eval(f.read())
			f.close()
			self.bias=l[0]
			self.model=l[1]
			self.res=list()
			self.recursiveRead()
			self.writeOutputFile()
			#self.PerformanceMatrix() ### UNCOMMENT ME ###

		except Exception as e:
			traceback.print_exc()
			print('Unexpected Error Encountered')

	def recursiveRead(self):
		for subdir, dirs, files in os.walk(self.path):
			for file in files:
				if file.endswith('.txt'):
					self.res.append(self.fileTest(os.path.join(subdir, file)))

	def fileTest(self,file):
		f=open(file,'r',encoding='latin1')		
		alpha=self.bias
		for x in f.read().split():
			alpha+=self.model.get(x,0)
		if alpha>0:
			return 'spam'+' '+file
		else:
			return 'ham'+' '+file

	def writeOutputFile(self):
		f=open(self.outputFile,'w',encoding='latin1')
		for x in self.res:
			f.write(x+'\n')
		f.close()

	def PerformanceMatrix(self):
		prediction=list()
		actual=list()
		correctSpam=0
		correctHam=0
		for subdir, dirs, files in os.walk(self.path):
			if subdir.endswith('spam'):
				for file in files:
					if file.endswith('.txt'):
						a=self.fileTest(os.path.join(subdir, file)).split(' ')[0]
						b='spam'
						if(a==b):
							correctSpam+=1
						prediction.append(a)
						actual.append(b)
						
			if subdir.endswith('ham'):
				for file in files:			
					if file.endswith('.txt'):
						a=self.fileTest(os.path.join(subdir, file)).split(' ')[0]
						b='ham'
						if(a==b):
							correctHam+=1
						prediction.append(a)
						actual.append(b)
		self.PerformanceCalculations(prediction,actual,correctHam,correctSpam)

	def PerformanceCalculations(self,prediction,actual,correctHam,correctSpam):
		p=Counter(prediction)
		a=Counter(actual)
		precision_ham=correctHam/dict(p)['ham']
		precision_spam=correctSpam/dict(p)['spam']
		recall_ham=correctHam/dict(a)['ham']
		recall_spam=correctSpam/dict(a)['spam']
		f1_ham=(2*precision_ham*recall_ham)/(precision_ham+recall_ham)
		f1_spam=(2*precision_spam*recall_spam)/(precision_spam+recall_spam)
		res=list()
		res.append('spam precision: '+str(round(precision_spam,2))+'\n')
		res.append('spam recall: '+str(round(recall_spam,2))+'\n')
		res.append('spam F1 score: '+str(round(f1_spam,2))+'\n')
		res.append('ham precision: '+str(round(precision_ham,2))+'\n')
		res.append('ham recall: '+str(round(recall_ham,2))+'\n')
		res.append('ham F1 score: '+str(round(f1_ham,2))+'\n')
		print(''.join(res))

#start_time = time.time()
#print(start_time)
perClassify(sys.argv[1],sys.argv[2])
#print("Classify Time: %s "%(time.time() - start_time))
#python per_classify.py "C:\Users\Xenon\Documents\GitHub\Natural-Language-Processing\Perceptron\Spam or Ham\dev" output.txt