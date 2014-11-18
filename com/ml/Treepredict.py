# coding:utf-8
'''
Created on 2014年11月6日

@author: Administrator
'''
from math import log
from PIL import Image, ImageDraw

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
        return decisionnode(results=uniqueCounts(rows))
        

def printTree(tree, indent=''):
    # 是否一个叶节点
    if tree.results != None:
        print str(tree.results)
    else:
        # 打印判断条件
        print str(tree.col) + ':' + str(tree.value) + '? '
        # 打印分支
        print indent + 'T->',
        printTree(tree.tb, indent + ' ')
        print indent + 'F->',
        printTree(tree.fb, indent + ' ')

def getWidth(tree):
    if tree.tb == None and tree.fb == None: 
        return 1
    return getWidth(tree.tb) + getWidth(tree.fb)

def getDepth(tree):
    if tree.tb == None and tree.fb == None: 
        return 0
    return max(getDepth(tree.tb), getDepth(tree.fb)) + 1

def drawtree(tree, jpeg='tree.jpg'):
    w = getWidth(tree) * 100
    h = getDepth(tree) * 100 + 120
    
    img = Image.new('RGB', (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    drawnode(draw, tree, w / 2, 20)
    img.save(jpeg, 'JPEG')
  
def drawnode(draw, tree, x, y):
    if tree.results == None:
        # 得到每个分支的宽度
        w1 = getWidth(tree.fb) * 100
        w2 = getWidth(tree.tb) * 100

        # 确定此节点所要占据的总空间
        left = x - (w1 + w2) / 2
        right = x + (w1 + w2) / 2
    
        # 绘制判断条件字符串
        draw.text((x - 20, y - 10), str(tree.col) + ':' + str(tree.value), (0, 0, 0))
    
        # 绘制到分支的连线
        draw.line((x, y, left + w1 / 2, y + 100), fill=(255, 0, 0))
        draw.line((x, y, right - w2 / 2, y + 100), fill=(255, 0, 0))
        
        # 绘制分支节点
        drawnode(draw, tree.fb, left + w1 / 2, y + 100)
        drawnode(draw, tree.tb, right - w2 / 2, y + 100)
    else:
        txt = ' \n'.join(['%s:%d' % v for v in tree.results.items()])
        draw.text((x - 20, y), txt, (0, 0, 0))
        

def classify(observation, tree):
    if tree.results != None:
        return tree.results
    else:
        v = observation[tree.col]
        branch = None
        if isinstance(v, int) or isinstance(v, float):
            if v >= tree.value:
                branch = tree.tb
            else:
                branch = tree.fb
        else:
            if v == tree.value:
                branch = tree.tb
            else:
                branch = tree.fb
        return classify(observation, branch)

def prune(tree, mingain):
    # If the branches aren't leaves, then prune them
    if tree.tb.results == None:
        prune(tree.tb, mingain)
    if tree.fb.results == None:
        prune(tree.fb, mingain)
    
      # If both the subbranches are now leaves, see if they
      # should merged
    if tree.tb.results != None and tree.fb.results != None:
        # Build a combined dataset
        tb, fb = [], []
        for v, c in tree.tb.results.items():
            tb += [[v]] * c
        for v, c in tree.fb.results.items():
            fb += [[v]] * c
    
        # Test the reduction in entropy
        delta = entropy(tb + fb) - (entropy(tb) + entropy(fb) / 2)

        if delta < mingain:
            # Merge the branches
            tree.tb, tree.fb = None, None
            tree.results = uniqueCounts(tb + fb)

def main():
    # uniqueCounts(TestData)
    # print entropy(TestData)
    # set1, set2 = divideset(TestData, 2, 'yes')
    # print giniimpurity(set1)
    # print entropy(set1)
    
    tree = buildTree(TestData, entropy)
    printTree(tree)
    # drawtree(tree, jpeg='treeview.jpg')
    print classify(['(direct)', 'USA', 'yes', 5], tree)
    prune(tree, 1.0)
    printTree(tree)

if __name__ == '__main__':
    main()
