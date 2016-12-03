import hw3_corpus_tool as tools
import sys
import os
import random
import glob
import pycrfsuite as crf

class baseline_crf(object):
	def __init__(self,inputDir,testDir,outputFile):
		self.inputDir=inputDir
		self.testDir=testDir
		self.outputFile=outputFile
		self.outputTags=list()
		validation=False
		if not validation:
			self.X_train,self.Y_train=self.readFiles(self.inputDir)
			self.TestFileNames=[[],[]]
			self.X_test,self.Y_test=self.readFiles(self.testDir,True)
			self.crfTrain()
			self.crfPredict()
			self.writeOutput()
			self.calculateAccuaracy()
		else:
			inputFiles=self.readInputDirectory()
			inputFilesData=list()
			for file in inputFiles:
				prev=None				
				utterances=tools.get_utterances_from_filename(file)
				l_uter=list()
				for utterance in utterances:
					utterances_X=list()
					current=utterance.speaker
					if prev==current:
						utterances_X.append('1')
					else:
						utterances_X.append('0')
					if prev==None:
						utterances_X.append('1')
					else:
						utterances_X.append('0')
					prev=current
					if utterance.pos:
						utterances_X.extend(self.utterance2features(utterance.pos))
					utterances_Y=utterance.act_tag
					l_uter.append([utterances_X,utterances_Y])
				inputFilesData.append(l_uter)
			l=[_ for _ in range(len(inputFiles))]
			random.shuffle(l)
			#print(inputFilesData[2][12])
			#return 
			n=len(l)/4
			for i in range(4):
				self.X_train=list()
				self.Y_train=list()
				self.X_test=list()
				self.Y_test=list()
				for j in range(i*n,(i+1)*n):
					ind=l[j]
					#print(ind)
					self.X_test.extend([x[0] for x in inputFilesData[ind]])
					#input(len(self.X_test))
					self.Y_test.extend([x[1] for x in inputFilesData[ind]])
					#print(ind)
					#input(self.Y_test)
				for j in range(0,i*n):
					ind=l[j]
					self.X_train.extend([x[0] for x in inputFilesData[ind]])
					self.Y_train.extend([x[1] for x in inputFilesData[ind]])
				for j in range((i+1)*n,len(l)):
					ind=l[j]
					self.X_train.extend([x[0] for x in inputFilesData[ind]])
					self.Y_train.extend([x[1] for x in inputFilesData[ind]])
				self.crfTrain()
				self.crfPredict()
				self.calculateAccuaracy()


	def readFiles(self,path,flag=False):
		X=list()
		Y=list()
		conversations=list(tools.get_data(path))
		for conversation in conversations:
			prev=None
			count=0
			for utterance in conversation[1]:
				count+=1
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
				self.TestFileNames[0].append(conversation[0])
				self.TestFileNames[1].append(count)
		return X,Y
		
	def crfTrain(self):
		trainer=crf.Trainer(verbose=False)
		trainer.append(self.X_train,self.Y_train)
		trainer.set_params({
			'c1':1.0,
			'c2':1e-3,
			'max_iterations':250,
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

	def crfPredict(self):
		tagger=crf.Tagger()
		tagger.open('baseline_model.crfsuite')
		self.outputTags=tagger.tag(self.X_test)

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

	def readInputDirectory(self):
		filenames = sorted(glob.glob(os.path.join(self.inputDir, "*.csv")))
		return filenames

baseline_crf(sys.argv[1],sys.argv[2],sys.argv[3])
#python baseline_crf.py /home/arpitnigam/Desktop/WinDocuments/GitHub/Natural-Language-Processing/CRF/labeled\ data/labeled\ data /home/arpitnigam/Desktop/WinDocuments/GitHub/Natural-Language-Processing/CRF/labeled\ data/unlabeled\ data output.txt
