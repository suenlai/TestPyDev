# coding:utf-8
'''
Created on 2014年11月6日

@author: Administrator
'''
from math import log

TestData = [['slashdot', 'USA', 'yes', 18, 'None'],
        ['google', 'France', 'yes', 23, 'Premium'],
        ['digg', 'USA', 'yes', 24, 'Basic'],
        ['kiwitobes', 'France', 'yes', 23, 'Basic'],
        ['google', 'UK', 'no', 21, 'Premium'],
        ['(direct)', 'New Zealand', 'no', 12, 'None'],
        ['(direct)', 'UK', 'no', 21, 'Basic'],
        ['google', 'USA', 'no', 24, 'Premium'],
        ['slashdot', 'France', 'yes', 19, 'None'],
        ['digg', 'USA', 'no', 18, 'None'],
        ['google', 'UK', 'no', 18, 'None'],
        ['kiwitobes', 'UK', 'no', 19, 'None'],
        ['digg', 'New Zealand', 'yes', 12, 'Basic'],
        ['slashdot', 'UK', 'no', 21, 'None'],
        ['google', 'UK', 'yes', 18, 'Basic'],
        ['kiwitobes', 'France', 'yes', 19, 'Basic']]

class decisionnode:
    def __init__(self, col= -1, value=None, results=None, tb=None, fb=None):
        self.col = col
        self.value = value
        self.results = results
        self.tb = tb
        self.fb = fb

# 在某一列上对数据结合进行拆分，能够处理数值类型数据或名词数据
def divideset(rows, column, value):
    # 定义一个函数，令其告诉我们数据行属于第一组（true）还是第二组（false）
    splitFunction = None
    if isinstance(value, int) or isinstance(value, float):
        splitFunction = lambda row:row[column] >= value
    else:
        splitFunction = lambda row:row[column] == value
        
    # 将数据集拆分成2个集合并返回
    set1 = [row for row in rows if splitFunction(row)]
    set2 = [row for row in rows if not splitFunction(row)]
    return (set1, set2)

# 对各种可能的结果进行计数（每一行数据的最后一列记录了这一计数结果）
def uniqueCounts(rows):
    results = {}
    for row in rows:
        # 计数结果在最后一列
        r = row[len(row) - 1]
        if r not in results:
            results[r] = 0
        results[r] += 1
    return results

# 随机防止的数据项出现于错误分类中的概率
def giniimpurity(rows):
    total = len(rows)
    counts = uniqueCounts(rows)
    imp = 0
    for i in counts:
        p1 = float(counts[i]) / total
        for j in counts:
            if i == j:
                continue
            p2 = float(counts[j]) / total
            imp += p1 * p2
    return imp

# 熵是遍历所有可能的结果之后得到的p(x)log(p(x))之和
def entropy(rows):
    log2 = lambda x:log(x) / log(2)
    results = uniqueCounts(rows)
    # 开始计算熵的值
    ent = 0.0
    for r in results.keys():
        p = float(results[r]) / len(rows)
        # ent = ent - p * log2(p)
        ent = ent - p * log(p, 2)  # 以2为底求对数
    return ent

def buildTree(rows, entropyScore=entropy):
    if len(rows) == 0:
        return decisionnode
    currentScore = entropyScore(rows)
    
    # 定义变量记录最佳拆分条件
    bestGain = 0.0
    bestCriteria = None
    bestSets = None
    
    columnCount = len(rows[0]) - 1
    
    for col in range(0, columnCount):
        # 在当前列中生成一个由不容值构成的序列
        columnValues = {}
        for row in rows:
            columnValues[row[col]] = 1
        # 根据这一列中的每个值，对数据集进行拆分
        for value in columnValues.keys():
            (set1, set2) = divideset(rows, col, value)
            
            # 信息增益
            p = float(len(set1)) / len(rows)
            gain = currentScore - p * entropyScore(set1) - (1 - p) * entropyScore(set2)
            if gain > bestGain and len(set1) > 0 and len(set2) > 0:
                bestGain = gain
                bestCriteria = (col, value)
                bestSets = (set1, set2)
    
    # 创建子分支
    if bestGain > 0:
        trueBranch = buildTree(bestSets[0])
        falseBranch = buildTree(bestSets[1])
        return decisionnode(col=bestCriteria[0], value=bestCriteria[1], tb=trueBranch, fb=falseBranch)
    else:
        return decisionnode(result=uniqueCounts(rows))
        
    

def main():
    # uniqueCounts(TestData)
    # print entropy(TestData)
    # set1, set2 = divideset(TestData, 2, 'yes')
    # print giniimpurity(set1)
    # print entropy(set1)
    
    buildTree(TestData, entropy)

if __name__ == '__main__':
    main()
