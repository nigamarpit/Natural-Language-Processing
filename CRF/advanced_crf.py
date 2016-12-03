import hw3_corpus_tool as tools
import sys
import os
import random
import glob
import pycrfsuite as crf

class advanced_crf(object):
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
			for i in range(len(conversation[1])):
				count+=1
				l=list()
				current=conversation[1][i].speaker
				if prev==current:
					l.append('1')
				else:
					l.append('0')
				if prev==None:
					l.append('1')
				else:
					l.append('0')
				prev=current

				if i!=len(conversation[1])-1 and current==conversation[1][i+1].speaker:
					l.append('1')
				else:
					l.append('0')

				if conversation[1][i].pos:
					l.extend(self.utterance2features(conversation[1][i].pos))
				X.append(l)
				Y.append(conversation[1][i].act_tag)
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
		trainer.train('advanced_model.crfsuite')


	def utterance2features(self,utterance):
		tokens=list()
		pos=list()
		ques='0'
		wh_ques='0'
		if len(utterance[0].token)>0 and utterance[0].token[0]=='W':
			wh_ques='1'
		for i in range(len(utterance)):
			if utterance[i].token=='?':
				ques='1'
			tokens.append(utterance[i].token.lower())
			pos.append(utterance[i].pos)

		tokenBigrams=list()
		posBigrams=list()

		for i in range(len(tokens)-1):
			tokenBigrams.append(tokens[i]+'|'+tokens[i+1])
			posBigrams.append(pos[i]+'|'+pos[i+1])

		tokenTrigrams=list()
		posTrigrams=list()
		for i in range(len(tokens)-2):
			tokenTrigrams.append(tokens[i]+'|'+tokens[i+1]+'|'+tokens[i+2])
			posTrigrams.append(pos[i]+'|'+pos[i+1]+'|'+pos[i+2])

		#tokens.insert(0,wh_ques)
		#tokens.insert(0,ques)
		'''
		if len(utterance)<10:
			tokens.insert(0,'1')
		elif len(utterance)<20:
			tokens.insert(0,'2')
		elif len(utterance)<30:
			tokens.insert(0,'3')
		elif len(utterance)<40:
			tokens.insert(0,'4')
		else:
			tokens.insert(0,'5')
		'''
		tokens.extend(pos)
		tokens.extend(tokenBigrams)
		tokens.extend(posBigrams)
		tokens.extend(tokenTrigrams)
		tokens.extend(posTrigrams)
		return tokens

	def crfPredict(self):
		tagger=crf.Tagger()
		tagger.open('advanced_model.crfsuite')
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

advanced_crf(sys.argv[1],sys.argv[2],sys.argv[3])
#python advanced_crf.py /home/arpitnigam/Desktop/WinDocuments/GitHub/Natural-Language-Processing/CRF/labeled\ data/labeled\ data /home/arpitnigam/Desktop/WinDocuments/GitHub/Natural-Language-Processing/CRF/labeled\ data/unlabeled\ data output.txt
