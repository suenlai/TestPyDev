# coding:utf-8
'''
Created on 2015年1月13日

@author: Administrator
'''

def loadDataSet():
    return [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]

def createList(dataSet):
    list = []
    for transaction in dataSet:
        for item in transaction:
            if not [item] in list:
                list.append([item])
                
    list.sort()  
    return map(frozenset, list)


def scanCandidateData(candidateData, list, minSupport):
    ssCnt = {}
    for tid in candidateData:  # 计算某个项出现的次数
        for can in list:
            if can.issubset(tid):
                if not ssCnt.has_key(can):
                    ssCnt[can] = 1
                else:
                    ssCnt[can] += 1
    
    numItems = float(len(candidateData))
    retList = []
    supportData = {}
    
    for key in ssCnt:
        support = ssCnt[key] / numItems
        if support >= minSupport:
            retList.insert(0, key)
        supportData[key] = support
    
    return retList, supportData
    
    
def generateApriori(Lk, k):
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i + 1, lenLk): 
            L1 = list(Lk[i])[:k - 2] #取列表中前k-2个数
            L2 = list(Lk[j])[:k - 2]
            L1.sort()
            L2.sort()
            if L1 == L2:  # if first k-2 elements are equal
                retList.append(Lk[i] | Lk[j])  # set union
                
    return retList

def apriori(dataSet, minSupport=0.5):
    list = createList(dataSet)
    candidateData = map(set, dataSet)
    L1, supportData = scanCandidateData(candidateData, list, minSupport)
    L = [L1]
    k = 2
    while(len(L[k - 2]) > 0):
        ck = generateApriori(L[k - 2], k)
        lk, sup = scanCandidateData(candidateData, ck, minSupport)
        supportData.update(sup)
        L.append(lk)
        k += 1
    
    return L, supportData


def generateRules(L, supportData, minConf=0.7):
    bigRuleList = []
    for i in range(1, len(L)):
        for freqSet in L[i]:
            H1 = [frozenset([item]) for item in freqSet]
            if (i > 1):
                rulesFromConseq(freqSet, H1, supportData, bigRuleList, minConf)
            else:
                calcConf(freqSet, H1, supportData, bigRuleList, minConf)

    return bigRuleList

#计算可信度
def calcConf(freqSet, H, supportData, brl, minConf=0.7):
    prunedH = []
    for conseq in H:
        conf = supportData[freqSet] / supportData[freqSet - conseq]
        if conf >= minConf: 
            print freqSet - conseq, '-->', conseq, 'conf:', conf
            brl.append((freqSet - conseq, conseq, conf))
            prunedH.append(conseq)
    return prunedH
        
def rulesFromConseq(freqSet, H, supportData, brl, minConf=0.7):
    m = len(H[0])
    if (len(freqSet) > (m + 1)):  # try further merging
        Hmp1 = generateApriori(H, m + 1)  # create Hm+1 new candidates
        Hmp1 = calcConf(freqSet, Hmp1, supportData, brl, minConf)
        if (len(Hmp1) > 1):  # need at least two sets to merge
            rulesFromConseq(freqSet, Hmp1, supportData, brl, minConf)
            

def main():
    dataSet = loadDataSet()
    '''
    list = createList(dataSet)
    print list
    candidateData = map(set, dataSet)
    L1, supportData = scanCandidateData(candidateData, list, 0.5)
    print L1
    '''
    L, supportData = apriori(dataSet)
    print L
    print supportData
    generateRules(L, supportData, minConf=0.3)
    
if __name__ == '__main__':
    main()
