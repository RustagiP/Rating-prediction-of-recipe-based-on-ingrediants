#!/usr/bin/python
# Project 1 (L645 : Problem 1)
# Author : Prerna Rustagi and Veer Singh
# Date : 10/16/2013

import sys;
import math;
import os;
import shutil;
import re;


global testDict
testDict = dict()
global trainDict
trainDict = dict()
global featureDict
featureDict = dict()
global unorderedDict
unorderedDict = dict()	
global ts
ts = "ts"
global arrayVal
arrayVal = []
global tableSpoon
tableSpoon = "tablespoon"
global cup
cup = "cup"
global stick
stick = "stick"
global sticks
sticks = "sticks"
global pound
pound = "pound"
global count
count = 1
global ounce
ounce = "ounce"
global ounces
ounces = "ounces"


### following function extracts recipe type from metadata and appends it to recipe filename
def modifyfileName():

        if not os.access("/N/u/rustagip/Quarry/ingred", os.F_OK):
                os.makedirs("/N/u/rustagip/Quarry/ingred")
        #def renamefile (filename,line):

        for filename in os.listdir("/N/u/rustagip/Quarry/meta/"):
                fname = '/N/u/rustagip/Quarry/meta/'+filename
                with open(fname) as f:
                        f=f.readlines()
                for line in f:
                        if "type:" in line:
                                line = str(line)
                                line = line.replace("type:"," ")
                                line = line.replace("/",",")
                                line = line.split(',')
                                line = line[len(line) -1 ]
                                line = line.strip()
                                sfname = '/N/u/rustagip/Quarry/ingredients/'+filename
                                if line == "Quick & Easy" or line == "Kid-Friendly" or line == "Entertaining":
                                        dfname = "/N/u/rustagip/Quarry/ingred/" + filename +"().txt"
                                else:
                                        dfname = "/N/u/rustagip/Quarry/ingred/" + filename + "(" + line + ").txt"
                                break;
                        elif "dietary considerations:" in line:
                                line = str(line)
                                line = line.replace("dietary considerations:"," ")
                                line = line.split(',')
                                line = line[0]
                                line = line.replace("/"," ")
                                line = line.strip()
                                sfname = '/N/u/rustagip/Quarry/ingredients/'+filename
                                dfname = "/N/u/rustagip/Quarry/ingred/" + filename + "(" + line + ").txt"
                                print line
                                break
        	f.close()
	        print dfname , sfname
                if os.path.isfile(sfname):
                        os.rename(sfname,dfname)

def createTrainTestDict():
    findFiles = "/N/u/rustagip/Quarry/reviews_ingr_instr_split"
    openFile = open(findFiles)
    count = 1
    for line in openFile:
        index = line.index(":")
        type = line[0:index]
        length = line.__len__()
        filename = line[index+1:length]
        if(type=="TRAIN"):
            trainDict[filename.strip()]=count
            count = count + 1
        elif(type=="TEST"):
            testDict[filename.strip()]=count
            count = count +1
    openFile.close()
    print "Finished createTrainTestDict()"

### This fucntion calls NLTK tagger and tags the data in the file and writes output in a newfile with same name
def readFile(file):
    import nltk
    import numpy
    openFile = open(file)
    lines = ""
    ins = file.split('/')
    writeFile = ins[ins.__len__()-1]
    f = open("/N/u/rustagip/Quarry/POS_tagged/"+writeFile,'w')
    for line in openFile:
        lines = line.strip()
        text = nltk.word_tokenize(lines)
        tags = nltk.pos_tag(text)
        string = str(tags)
        f.write(string) # python will convert \n to os.linesep
        f.write("\n")
    openFile.close()
    f.close()

#### Follwoing fucntion calls readFile function for each file in the directory
def checkFiles():

    directory = "/N/u/rustagip/Quarry/ingred/"

    for filename in os.listdir(directory):
        readFile(directory + filename)

### following fucntion extract data from tagged files
def createFeatureSet():
    print "start createFeatureSet()"
    count =1
    directory = "/N/u/rustagip/Quarry/POS_tagged/"
    #directory = "/N/u/rustagip/Quarry/test/"
    files = os.listdir(directory)	
    for filename in files:
#	print filename
        if filename[0:filename.index('(')] in trainDict:
#		print "HEllo start createFeatureSet()"
                openFile = open(directory+str(filename))

                lines = ""

                #ins = openFile.split('\n')

                for line in openFile:
                #print line
                        finalFeature=""
                        ins = line.split(",")
                        length = ins.__len__()
                        #print "1:   "+line

                        #check if there is a measure for the ingredient
                        measure = re.sub('[^A-Za-z0-9]+', '', str(ins[length-2])).lower()

                        #check if there is a measure
                        if(measure==ts or measure==tableSpoon or measure==cup or measure==pound or measure==sticks or measure==stick or measure==ounce or measure==ounces):

                                #for loop to iterate over the line extract features
                                for x in range(0,length-1):
                                        feature=""
                                        tagCompare=re.sub('[^A-Za-z0-9]+', '', str(ins[x])).lower()
                                        valCompare=re.sub('[^A-Za-z0-9]+', '', str(ins[x-1])).lower()
                                        #print tagCompare
                                        #print valCompare
                                        if((tagCompare=="nn" or tagCompare=="nns" or tagCompare=="jj") and valCompare!=ts and valCompare!=tableSpoon and valCompare!=pound and valCompare!=cup
                                    and valCompare!=stick and valCompare!=sticks and valCompare!=ounce and valCompare!=ounces):
                                                feature=feature+valCompare

                                        finalFeature=finalFeature+feature

                                if(finalFeature in featureDict.values()):
                                        d=1
                                else:
                                        featureDict[count]=finalFeature.lower()
                                        count=count+1
		openFile.close()
    directory = "/N/u/rustagip/Quarry/POS_tagged/"
    count = count + 1
    files = os.listdir(directory)
    for filename in files:
       	if filename[0:filename.index('(')] in trainDict:
    		start = filename.index('(') + 1
                end = filename.index(')')
                finalFeature = filename[start:end].lower()
                if(finalFeature not in featureDict.values()):
                	featureDict[count] = finalFeature.lower()
                        count = count + 1
    #writeFeatureFile(trainDict,"trainFile",1)
    #writeFeatureFile(testDict,"testFile",1)
    print featureDict

def writeFeatureFile(dict,inputFile,type):
    import collections
    print "writeFeatureFile()"	
    #extarct feature and write into input file for SVM
    directory = "/N/u/rustagip/Quarry/POS_tagged/"
    cdVal = 0.0
    f = open("/N/u/rustagip/Quarry/outputNLTK/"+inputFile, 'w')
    files = os.listdir(directory)
    print dict
    for filename in files:
        if filename[0:filename.index('(')] in dict:
                file = directory + filename
                openFile = open(file)
		unorderedDict.clear()
  		print unorderedDict	
                lines = ""
                f.write('\n')
		f.write(str(filename[0] + ' '))
		if type == 1 :
			start = filename.index('(') + 1
        		end = filename.index(')')
        		finalFeature = filename[start:end].lower()
                        if finalFeature in featureDict.values():
				for tempkey in featureDict.keys():
					if featureDict[tempkey] == finalFeature:
						key = tempkey
						print finalFeature + ':' + str(1)
				if key not in unorderedDict.keys():
					unorderedDict[key] = 1
		
		for line in openFile:
                    finalFeature=""
                    ins = line.split(",")
                    length = ins.__len__()
                    #check if there is a measure for the ingredient
                    measure = re.sub('[^A-Za-z0-9]+', '', str(ins[length-2])).lower()
                    #check if there is a measure
                    if(measure==ts or measure==tableSpoon or measure==cup or measure==pound or measure==sticks or measure==stick or measure==ounce or measure==ounces):
                        #for loop to iterate over the line extract features
                        for x in range(0,length-1):
                            feature=""
                            tagCompare=re.sub('[^A-Za-z0-9]+', '', str(ins[x])).lower()
                            valCompare=re.sub('[^A-Za-z0-9]+', '', str(ins[x-1])).lower()
                            #print tagCompare
                            #print valCompare
                            if((tagCompare=="nn" or tagCompare=="nns" or tagCompare=="jj") and valCompare!=ts and valCompare!=tableSpoon and valCompare!=pound and valCompare!=cup
                            and valCompare!=stick and valCompare!=sticks and valCompare!=ounce and valCompare!=ounces):
                                feature=feature+valCompare

                            finalFeature=finalFeature+feature
			
                        if(finalFeature in featureDict.values()):
                            
			    arrayVal = re.findall('\d+', line)
			    numlist = map(int, arrayVal)
			    if len(arrayVal)==0:
			    	cdVal = 1
			    else :		
                            	cdVal = sum(numlist)/float(len(arrayVal))
			    for tempkey in featureDict.keys():
				if featureDict[tempkey] == finalFeature:
                           	 	 key = tempkey
                            finalCdVal = Constants(cdVal,measure)
			    unorderedDict[key] = finalCdVal 	
			    #f.write(str(key) + ':' + str(finalCdVal) + ' ')
                            #Write key and finalCdVal into a file
	#	openFile.close()
        	od = collections.OrderedDict(sorted(unorderedDict.items()))
		for x in od.keys():
		#print od[x]
			f.write(str(x) + ':' + str(od[x]) + ' ')
	#f.close()

			


#### this function converts all measures into a normalized value
def Constants(cd, type):
    #1 cup = 16 ts
    #2 cups = 1 pound
    #32 ts = 1 pound
    #2 sticks of butter is 1 cup
    #1 oounce = 2 ts

    if(type==cup):
        value = cd*16
        type = ts
    elif(type==pound):
        value = cd*32
        type = ts
    elif(type==stick or type==sticks):
        value = cd*8
        type = ts
    elif(type==ounce or type==ounces):
        value = cd*2
    else:
        value = cd
        type = ts
    return value
    print ""


def wrapper():
    import os
    import re
    directory = "/N/u/rustagip/Quarry/POS_tagged/"
    typeDict = dict()
    c = 0
    for filename in os.listdir(directory):
            if filename[0:filename.index('(')] in trainDict:
                    start = filename.index('(') + 1
                    end = filename.index(')')
                    finalFeature = filename[start:end].lower()
                    if(finalFeature not in typeDict.values()):
                            typeDict[c] = finalFeature
                            c = c + 1
    print typeDict		
    for filename in os.listdir(directory):
    	    start = filename.index('(') + 1
            end = filename.index(')')
            finalFeature = filename[start:end].lower()
	    name = filename[0:start-1]
	    if finalFeature in typeDict.values():
		if int(filename[0]) != 0:
			if finalFeature == '':
				finalFeature = 'undefined';
			if name in trainDict:
				writeCategoryFile(directory,filename,finalFeature+'_train')
			elif name in testDict:
				writeCategoryFile(directory,filename,finalFeature+'_test')


def writeCategoryFile(directory,filename,inputFile):
		import collections
		f = open("/N/u/rustagip/Quarry/outputNLTK/"+inputFile, 'a')
	 	file = directory + filename
		print filename + inputFile
                openFile = open(file)
                unorderedDict.clear()
                print unorderedDict
                lines = ""
                f.write(str(filename[0] + ' '))
                for line in openFile:
                    finalFeature=""
                    ins = line.split(",")
                    length = ins.__len__()
                    #check if there is a measure for the ingredient
                    measure = re.sub('[^A-Za-z0-9]+', '', str(ins[length-2])).lower()
                    #check if there is a measure
                    if(measure==ts or measure==tableSpoon or measure==cup or measure==pound or measure==sticks or measure==stick or measure==ounce or measure==ounces):
                        #for loop to iterate over the line extract features
                        for x in range(0,length-1):
                            feature=""
                            tagCompare=re.sub('[^A-Za-z0-9]+', '', str(ins[x])).lower()
                            valCompare=re.sub('[^A-Za-z0-9]+', '', str(ins[x-1])).lower()
                            #print tagCompare
                            #print valCompare
                            if((tagCompare=="nn" or tagCompare=="nns" or tagCompare=="jj") and valCompare!=ts and valCompare!=tableSpoon and valCompare!=pound and valCompare!=cup
                            and valCompare!=stick and valCompare!=sticks and valCompare!=ounce and valCompare!=ounces):
                                feature=feature+valCompare

                            finalFeature=finalFeature+feature

                        if(finalFeature in featureDict.values()):

                            arrayVal = re.findall('\d+', line)
                            numlist = map(int, arrayVal)
                            if len(arrayVal)==0:
                                cdVal = 1
                            else :
                                cdVal = sum(numlist)/float(len(arrayVal))
                            for tempkey in featureDict.keys():
                                if featureDict[tempkey] == finalFeature:
                                         key = tempkey
                            finalCdVal = Constants(cdVal,measure)
                            unorderedDict[key] = finalCdVal
                            #f.write(str(key) + ':' + str(finalCdVal) + ' ')
                            #Write key and finalCdVal into a file
                openFile.close()
                od = collections.OrderedDict(sorted(unorderedDict.items()))
                for x in od.keys():
                #print od[x]
                        f.write(str(x) + ':' + str(od[x]) + ' ')
                f.write('\n')
		f.close()
	
			
        				
   


#modifyfileName()
#checkFiles()
createTrainTestDict()
createFeatureSet()
wrapper()

