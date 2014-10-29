# coding:utf-8
'''
Created on 2014年9月11日

@author: Administrator
'''
from numpy import *

def loadDataSet():
    postingList=[['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                 ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                 ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                 ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                 ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                 ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    classVec = [0,1,0,1,0,1]    #1 is abusive, 0 not
    return postingList,classVec

#创建一个包含在所有文档中不重复词的列表
def createVocabList(dataSet):
    vocabSet = set([])  #create empty set
    for document in dataSet:
        vocabSet = vocabSet | set(document) #union of the two sets
    return list(vocabSet)

#输入参数为词汇表及某个文档，输出是文档向量，向量的每一个元素是1或0，分别表示词汇表中的单词在输入文档中是否出现
def setOfWords2Vec(vocabList, inputSet):
    returnVec = [0]*len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
        else: print "the word: %s is not in my Vocabulary!" % word
    return returnVec

def trainNB0(trainMatrix,trainCategory):
    numTrainDocs = len(trainMatrix)
    numWords = len(trainMatrix[0])
    pAbusive = sum(trainCategory)/float(numTrainDocs)
    p0Num = ones(numWords); p1Num = ones(numWords)      #change to ones() 
    p0Denom = 2.0; p1Denom = 2.0                        #change to 2.0
    for i in range(numTrainDocs):
        if trainCategory[i] == 1:
            p1Num += trainMatrix[i]
            p1Denom += sum(trainMatrix[i])
        else:
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])
    p1Vect = log(p1Num/p1Denom)          #change to log()
    p0Vect = log(p0Num/p0Denom)          #change to log()
    return p0Vect,p1Vect,pAbusive

#朴素贝叶斯分类器  
def classifyNB(vec2Classify, p0Vec, p1Vec, pClass1):  
    p1 = sum(vec2Classify*p1Vec) + log(pClass1)  
    p0 = sum(vec2Classify*p0Vec) + log(1.0-pClass1)  
    if p1 > p0:  
        return 1  
    else: return 0
    

#过滤垃圾邮件  
def textParse(bigString):      #正则表达式进行文本解析  
    import re  
    listOfTokens = re.split(r'\W*',bigString)  
    return [tok.lower() for tok in listOfTokens if len(tok) > 2]  
  
def spamTest():  
    docList = []; classList = []; fullText = []  
    for i in range(1,26):                          #导入并解析文本文件  
        wordList = textParse(open('D:\\workspace\\TestPyDev\\email\\spam\\%d.txt' % i).read())  
        docList.append(wordList)  
        fullText.extend(wordList)  
        classList.append(1)  
        wordList = textParse(open('D:\\workspace\\TestPyDev\\email\\ham/%d.txt' % i).read())  
        docList.append(wordList)  
        fullText.extend(wordList)  
        classList.append(0)  
    vocabList = createVocabList(docList)  
    trainingSet = range(50);testSet = []  
    for i in range(10):                         #随机构建训练集  
        randIndex = int(random.uniform(0,len(trainingSet)))  
        testSet.append(trainingSet[randIndex])  
        del(trainingSet[randIndex])  
    trainMat = []; trainClasses = []  
    for docIndex in trainingSet:  
        trainMat.append(setOfWords2Vec(vocabList, docList[docIndex]))  
        trainClasses.append(classList[docIndex])  
    p0V, p1V, pSpam = trainNB0(array(trainMat), array(trainClasses))  
    errorCount = 0  
    for docIndex in testSet:              #对测试集进行分类  
        wordVector = setOfWords2Vec(vocabList, docList[docIndex])  
        if classifyNB(array(wordVector), p0V, p1V, pSpam) != classList[docIndex]:  
            errorCount += 1  
    print 'the error rate is: ', float(errorCount)/len(testSet)      

def main():
    '''
    listOposts, listClasses = loadDataSet()
    myVocabList = createVocabList(listOposts)
    #print myVocabList
    
    #print setOfWords2Vec(myVocabList, listOposts[0])
    
    trainMat = []
    for postinDoc in listOposts:
        trainMat.append(setOfWords2Vec(myVocabList, postinDoc))
        
    p0V, p1V, pAb = trainNB0(trainMat, listClasses)
    
    testEntry = ['love','my','dalmation']  
    thisDoc = array(setOfWords2Vec(myVocabList, testEntry))  
    print testEntry, 'classified as: ', classifyNB(thisDoc, p0V, p1V, pAb)  
    '''
    
    spamTest()
    

if __name__ == '__main__':
    main()