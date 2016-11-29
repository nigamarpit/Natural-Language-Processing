import hw3_corpus_tool as tools
import sys
import os
import pycrfsuite as crf

class baseline_crf(object):
	def __init__(self,inputDir,testDir,outputFile):
		self.inputDir=inputDir
		self.testDir=testDir
		self.outputFile=outputFile
		self.outputTags=list()
		#print(self.inputDir)
		#print(self.testDir)
		#print(self.outputFile)
		#return
		#self.X_train=list()
		#self.Y_train=list()
		#self.X_test=self.X_train
		#self.Y_test=list()
		self.X_train,self.Y_train=self.readFiles(self.inputDir)
		self.TestFileNames=[[],[]]
		self.X_test,self.Y_test=self.readFiles(self.testDir,True)
		#print(self.TestFileNames)
		#print(self.X_test)
		#print(self.Y_test)
		self.crfTrain()
		self.crfPredict()
		self.writeOutput()
		#self.calculateAccuaracy()

	def readFiles(self,path,flag=False):
		#files=list()
		#print(len(conversations))
		X=list()
		Y=list()
		conversations=list(tools.get_data(path))
		for conversation in conversations:
			prev=None
			count=0
			for utterance in conversation[1]:
				count+=1
				#input(utterance)
				l=list()
				current=utterance.speaker
				if prev==current:
					l.append('1')
				else:
					l.append('0')
				if prev==None:
					l.append('1')
				else:
					l.append('0')
				prev=current
				if utterance.pos:
					l.extend(self.utterance2features(utterance.pos))
				X.append(l)
				Y.append(utterance.act_tag)
			if flag:
				#print(conversation[0]+'\t'+str(count))
				self.TestFileNames[0].append(conversation[0])
				self.TestFileNames[1].append(count)
		return X,Y
		#print(conversation)
		#print(conversation[0].pos[0].token)
		#print(conversation[0].pos[0].pos)
		'''		
		for (dirpath, dirnames, filenames) in os.walk(self.inputDir):
			for filename in filenames:
				if filename.endswith('.csv'):
					files.append(os.path.join(dirpath,filename))
		'''
	def crfTrain(self):
		trainer=crf.Trainer(verbose=False)
		#for xseq,yseq in zip(self.X_train,self.Y_train):
		#	trainer.append(xseq,yseq)
		trainer.append(self.X_train,self.Y_train)
		trainer.set_params({
			'c1':1.0,
			'c2':1e-3,
			'max_iterations':50,
			'feature.possible_transitions':True
			})
		trainer.train('baseline_model.crfsuite')


	def utterance2features(self,utterance):
		tokens=list()
		pos=list()
		for i in range(len(utterance)):
			tokens.append(utterance[i].token)
			pos.append(utterance[i].pos)
		tokens.extend(pos)
		return tokens
		#return [self.word2features(conversation,i) for i in range(len(conversation))]

	def crfPredict(self):
		tagger=crf.Tagger()
		tagger.open('baseline_model.crfsuite')
		#for x in self.X_test:
		self.outputTags=tagger.tag(self.X_test)
		#print(len(self.outputTags))

	def calculateAccuaracy(self):
		total=len(self.Y_test)
		print(total)
		l=list()
		c=0
		for i in range(len(self.outputTags)):
			if self.outputTags[i]==self.Y_test[i]:
				l.append(True)
				c+=1
			else:
				l.append(False)
		print(c)
		print((c*100)/(total*1.0))

	def writeOutput(self):
		
		#for i in range(len(self.outputTags)):
		#	f.write(self.outputTags[i]+'\n')
		l=list()
		c=0
		for i in range(len(self.TestFileNames[0])):
			l.append('Filename="'+self.TestFileNames[0][i]+'"\n')
			for j in range(self.TestFileNames[1][i]):
				l.append(self.outputTags[c]+'\n')
				c+=1
			l.append('\n')
		f=open(self.outputFile,'w')
		for x in l:
			f.write(x)
		f.close()


	#def word2features(self,)		

baseline_crf(sys.argv[1],sys.argv[2],sys.argv[3])
#python baseline_crf.py /home/arpitnigam/Desktop/WinDocuments/GitHub/Natural-Language-Processing/CRF/labeled\ data/labeled\ data /home/arpitnigam/Desktop/WinDocuments/GitHub/Natural-Language-Processing/CRF/labeled\ data/unlabeled\ data output.txt
