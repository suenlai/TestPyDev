# coding:utf-8
'''
Created on 2015年1月14日

@author: Administrator
'''
class treeNode:
    def __init__(self, nameValue, numOccur, parentNode):
        self.name = nameValue
        self.count = numOccur
        self.nodeLink = None
        self.parent = parentNode  # needs to be updated
        self.children = {} 
    
    def inc(self, numOccur):
        self.count += numOccur
        
    def disp(self, ind=1):
        print '  ' * ind, self.name, ' ', self.count
        for child in self.children.values():
            child.disp(ind + 1)

def loadSimpData():
    simpDat = [['r', 'z', 'h', 'j', 'p'],
               ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
               ['z'],
               ['r', 'x', 'n', 'o', 's'],
               ['y', 'r', 'x', 'z', 'q', 't', 'p'],
               ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']]
    return simpDat

def createInitSet(dataSet):
    retDict = {}
    for trans in dataSet:
        retDict[frozenset(trans)] = 1
    return retDict

def createTree(dataSet, minSupport=1):
    headerTable = {}
    for trans in dataSet:  # 遍历数据集并统计每个元素项出现的频度，存储在头指针表中
        # print dataSet[trans]
        for item in trans:
            headerTable[item] = headerTable.get(item, 0) + dataSet[trans]
    
    for k in headerTable.keys():  # 删除不满足最小支持度的项
        if headerTable[k] < minSupport:
            del(headerTable[k])
            
    freqItemSet = set(headerTable.keys())  # 建立频繁集项
    if len(freqItemSet) == 0:
        return None, None
    
    for k in headerTable:  # 扩展头指针，保存计数值和指向每种类型第1个元素的指针
        headerTable[k] = [headerTable[k], None]
        
    retTree = treeNode('Null Set', 1, None)  # 建立根节点
    for tranSet, count in dataSet.items():  # 遍历数据集，
        localID = {}
        for item in tranSet:
            if item in freqItemSet:  # 只考虑频繁集项
                localID[item] = headerTable[item][0]
            
        if len(localID) > 0:
            orderedItems = [v[0] for v in sorted(localID.items(), key=lambda p:p[1], reverse=True)]
            updateTree(orderedItems, retTree, headerTable, count)
            
    return retTree, headerTable

def updateTree(items, inTree, headerTable, count):
    if items[0] in inTree.children:#是否在子节点中
        inTree.children[items[0]].inc(count)
    else:
        inTree.children[items[0]] = treeNode(items[0], count, inTree)#创建一个新节点
        if headerTable[items[0]][1] == None:  # 头指针的第1个元素是空，就指向新建的树节点
            headerTable[items[0]][1] = inTree.children[items[0]]
        else:
            updateHeader(headerTable[items[0]][1], inTree.children[items[0]])
    
    if len(items) > 1:  # items大于1继续构建树
        updateTree(items[1::], inTree.children[items[0]], headerTable, count)
        
def updateHeader(headerTableNode, targetNode):
    while (headerTableNode.nodeLink != None):
        headerTableNode = headerTableNode.nodeLink
    headerTableNode.nodeLink = targetNode

def ascendTree(leafNode, prefixPath):
    if leafNode.parent != None:
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.parent, prefixPath)
        
def findPrefixPath(basePat, treeNode):
    condPats = {}
    while treeNode != None:
        prefixPath = []
        ascendTree(treeNode, prefixPath)
        if len(prefixPath) > 1:
            condPats[frozenset(prefixPath[1:])] = treeNode.count
        treeNode = treeNode.nodeLink
    
    return condPats

def mineTree(inTree, headerTable, minSup, preFix, freqItemList):
    bigL = [v[0] for v in sorted(headerTable.items(), key=lambda p: p[1])]#对headerTable排序，从小到大
    for basePat in bigL:  
        newFreqSet = preFix.copy()
        newFreqSet.add(basePat)
        #将每一个频繁项添加到频繁项集列表
        freqItemList.append(newFreqSet)
        condPattBases = findPrefixPath(basePat, headerTable[basePat][1])
        #创建树
        myCondTree, myHead = createTree(condPattBases, minSup)
        
        if myHead != None: #3. mine cond. FP-tree
            #print 'conditional tree for: ',newFreqSet
            #myCondTree.disp(1)            
            mineTree(myCondTree, myHead, minSup, newFreqSet, freqItemList)
            

def main():
    '''
    rootNode = treeNode('pyramid', 9, None)
    rootNode.children['eye'] = treeNode('eye', 13, None)
    rootNode.disp()
    '''
    initDataSet = loadSimpData()
    dataSet = createInitSet(initDataSet)
    myFpTree, myHeaderTable = createTree(dataSet, 3)
    
    '''
    print myFpTree.disp()
    print findPrefixPath('t', myHeaderTable['t'][1])
    '''
    freqItems = []
    mineTree(myFpTree, myHeaderTable, 3, set([]), freqItems)
    print freqItems
    
    
if __name__ == '__main__':
    main()
