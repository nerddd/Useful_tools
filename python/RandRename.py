import random
import os

existName=[]
def renameRand(path):
	fileList=os.listdir(path)
	rangeLetter=('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
	for oldFileNameAndExt in fileList:
		newFileName=random.choice(rangeLetter)+random.choice(rangeLetter)+str(random.randrange(10))+str(random.randrange(10))+random.choice(rangeLetter)+str(random.randrange(10))
		while newFileName.upper() in existName:
			newFileName=random.choice(rangeLetter)+random.choice(rangeLetter)+str(random.randrange(10))+str(random.randrange(10))+random.choice(rangeLetter)+str(random.randrange(10))
		existName.append(newFileName.upper())
		[oldFileName,fileExt]=oldFileNameAndExt.split('.',1)
		newFileNameAndExt=[newFileName,fileExt]
		newFileNameAndExt='.'.join(newFileNameAndExt)
		path=os.path.abspath(path)
		pathSrc=path+'\\'+oldFileNameAndExt
		pathDst=path+'\\'+newFileNameAndExt
		os.rename(pathSrc,pathDst)

if __name__=='__main__':
	renameRand('./')