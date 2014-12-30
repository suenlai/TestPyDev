# coding:utf-8
'''
Created on 2014年12月25日

@author: kevin
'''

import operator
import matplotlib.pyplot as plt
from math import log


def createDataSet():
    dataSet = [[1, 1, 'yes'],
               [1, 1, 'yes'],
               [1, 0, 'no'],
               [0, 1, 'no'],
               [0, 1, 'no']]
    labels = ['no surfacing', 'flippers']
    return dataSet, labels

# 计算熵
def calcEntropy(dataSet):
    numEnteries = len(dataSet)
    labelCounts = {}
    
    for featVct in dataSet:
        currentLabel = featVct[-1]
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
    entropy = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key]) / numEnteries
        entropy -= prob * log(prob, 2)
    
    return entropy


# 划分数据集
def splitDataSet(dataSet, axis, value):
    retDateSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]  # 抽取数据
            reducedFeatVec.extend(featVec[axis + 1:])
            retDateSet.append(reducedFeatVec)
    
    return retDateSet

def chooseBestFeatureToSplit(dataSet):
    numFeatures = len(dataSet[0]) - 1
    baseEntropy = calcEntropy(dataSet)
    bestEntropy = 0.0;
    bestFeature = -1
    
    for i in range(numFeatures):
        featList = [example[i] for example in dataSet]
        uniqueValues = set(featList)  # 创建一个不重复的值
        newEntropy = 0.0
        
        for value in uniqueValues:  # 计算每种划分方式的信息熵
            subDataSet = splitDataSet(dataSet, i, value)
            prob = len(subDataSet) / float(len(dataSet))
            newEntropy += prob * calcEntropy(subDataSet)
        
        infoEntropy = baseEntropy - newEntropy
        
        if (infoEntropy > bestEntropy):  # 计算最好的信息增益
            bestEntropy = infoEntropy
            bestFeature = i
        
    return bestFeature


def majorityCnt(classList):
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]

def creatTree(dataSet, labels):
    classList = [example[-1] for example in dataSet]
    # print classList[0]
    # print classList.count(classList[2])
    if classList.count(classList[0]) == len(classList):
        return classList[0]
    if len(dataSet[0]) == 1:
        return majorityCnt(classList)
    
    bestFeat = chooseBestFeatureToSplit(dataSet)
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel:{}}
    del(labels[bestFeat])
    
    featValues = [example[bestFeat] for example in dataSet]
    uniqueValues = set(featValues)
    for value in uniqueValues:
        subLabels = labels[:]
        myTree[bestFeatLabel][value] = creatTree(splitDataSet(dataSet, bestFeat, value), subLabels)
    
    return myTree


# 叶节点的数目
def getTreeLeafs(myTree):
    leafs = 0
    #print myTree.keys()
    firstStr = myTree.keys()[0]
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict':  # 判断节点的数据类型是否为字典
            leafs += getTreeLeafs(secondDict[key])
        else:
            leafs += 1
    return leafs

# 树的层数
def getTreeDepth(myTree):
    maxDepth = 0
    firstStr = myTree.keys()[0]
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict':  # 判断节点的数据类型是否为字典
            thisDepth = 1 + getTreeDepth(secondDict[key])
        else:
            thisDepth = 1
        
        if thisDepth > maxDepth:
            maxDepth = thisDepth
    
    return maxDepth

decisionNode = dict(boxstyle="sawtooth", fc="0.8")
leafNode = dict(boxstyle="round4", fc="0.8")
arrow_args = dict(arrowstyle="<-")

def plotNode(nodeTxt, centerPt, parentPt, nodeType):
    createPlot.ax1.annotate(nodeTxt, xy=parentPt, xycoords='axes fraction',
             xytext=centerPt, textcoords='axes fraction',
             va="center", ha="center", bbox=nodeType, arrowprops=arrow_args)

# 
def plotMidText(cntPt, parentPt, text):
    xMid = (parentPt[0] - cntPt[0]) / 2.0 + cntPt[0]
    yMid = (parentPt[1] - cntPt[1]) / 2.0 + cntPt[1]
    createPlot.ax1.text(xMid, yMid, text, va="center", ha="center", rotation=30)
    
def plotTree(myTree, parentPt, nodeTxt):  # if the first key tells you what feat was split on
    numLeafs = getTreeLeafs(myTree)  # this determines the x width of this tree
    depth = getTreeDepth(myTree)
    firstStr = myTree.keys()[0]  # the text label for this node should be this
    cntPt = (plotTree.xOff + (1.0 + float(numLeafs)) / 2.0 / plotTree.totalW, plotTree.yOff)
    plotMidText(cntPt, parentPt, nodeTxt)
    plotNode(firstStr, cntPt, parentPt, decisionNode)
    secondDict = myTree[firstStr]
    plotTree.yOff = plotTree.yOff - 1.0 / plotTree.totalD
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict':  # test to see if the nodes are dictonaires, if not they are leaf nodes   
            plotTree(secondDict[key], cntPt, str(key))  # recursion
        else:  # it's a leaf node print the leaf node
            plotTree.xOff = plotTree.xOff + 1.0 / plotTree.totalW
            plotNode(secondDict[key], (plotTree.xOff, plotTree.yOff), cntPt, leafNode)
            plotMidText((plotTree.xOff, plotTree.yOff), cntPt, str(key))
    plotTree.yOff = plotTree.yOff + 1.0 / plotTree.totalD
    
def createPlot(inTree):
    fig = plt.figure(1, facecolor='white')
    fig.clf()
    axprops = dict(xticks=[], yticks=[])
    createPlot.ax1 = plt.subplot(111, frameon=False, **axprops)  # no ticks
    # createPlot.ax1 = plt.subplot(111, frameon=False) #ticks for demo puropses 
    plotTree.totalW = float(getTreeLeafs(inTree))
    plotTree.totalD = float(getTreeDepth(inTree))
    plotTree.xOff = -0.5 / plotTree.totalW; plotTree.yOff = 1.0;
    plotTree(inTree, (0.5, 1.0), '')
    plt.show()
  
def retrieveTree(i):
    listOfTrees = [{'no surfacing': {0: 'no', 1: {'flippers': {0: 'no', 1: 'yes'}}}},
                  {'no surfacing': {0: 'no', 1: {'flippers': {0: {'head': {0: 'no', 1: 'yes'}}, 1: 'no'}}}}
                  ]
    return listOfTrees[i]
  
def classify(inputTree, featLabels, testVec):
    firstStr = inputTree.keys()[0]
    secondDict = inputTree[firstStr]
    featIndex = featLabels.index(firstStr)
    key = testVec[featIndex]
    valueOfFeat = secondDict[key]
    if isinstance(valueOfFeat, dict): 
        classLabel = classify(valueOfFeat, featLabels, testVec)
    else: 
        classLabel = valueOfFeat
        
    return classLabel

def storeTree(inputTree, filename):
    import pickle
    fw = open(filename, 'w')
    pickle.dump(inputTree, fw)
    fw.close()
    
def loadTree(filename):
    import pickle
    fr = open(filename)
    return pickle.load(fr)

def main():
    myData, labels = createDataSet();
    print myData
    # print calcEntropy(myData)
    # print splitDataSet(myData, 0, 1)
    # print chooseBestFeatureToSplit(myData)
    
    
    #myTree = creatTree(myData, labels)
    '''
    print getTreeLeafs(myTree)
    print getTreeDepth(myTree)

    createPlot(myTree)
    
    '''
    myTree = retrieveTree(0)
    print myTree
    print classify(myTree, labels, [1, 0])
    
    
    '''
    import os
    #os.chdir("../..")
    #filePath = os.getcwd() + '\\res\\classifierStorage.txt'
    #storeTree(myTree, filePath)
    #print loadTree(filePath)
    filePath = os.getcwd() + '\\res\\lenses.txt'
    fr = open(filePath)
    lenses = [inst.strip().split('\t') for inst in fr.readlines()]
    lensesLabels = ['age', 'prescript', 'astigmatic', 'tearRate']
    lensesTree = creatTree(lenses, lensesLabels)
    print lensesTree
    createPlot(lensesTree)
    '''

if __name__ == '__main__':
    main()
