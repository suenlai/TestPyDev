# coding:utf-8
'''
Created on 2014年11月3日

@author: kevin
贝叶斯和费舍尔分类器
'''
import math

class Classifier:
    '''
    classdocs
    '''


    def __init__(self, getfeatures, filename=None):
        # 统计特征/分类组合的数量
        self.fc = {}
        # 统计每个分类中的文档数量
        self.cc = {}
        self.getfeatures = getfeatures
        
    # 增加对特征/分类组合计数
    def incf(self, f, cat):
        self.fc.setdefault(f, {})
        self.fc[f].setdefault(cat, 0)
        self.fc[f][cat] += 1

    # 增加对某一分类的计数值
    def incc(self, cat):
        self.cc.setdefault(cat, 0)
        self.cc[cat] += 1
        
    # 某一特征出现与某一分类中的次数
    def fcount(self, f, cat):
        if f in self.fc and cat in self.fc[f]:
            return float(self.fc[f][cat])
        return 0
    
    # 属于某一分类的内容项数量
    def catCount(self, cat):
        if cat in self.cc:
            return float(self.cc[cat])
        return 0

    # 所有内容项的数量
    def totalCount(self):
        return sum(self.cc.values())
    
    # 所有分类的列表
    def categories(self):
        return self.cc.keys()
    
    def train(self, item, cat):
        features = self.getfeatures(item)
        # 针对该分类为每个特征增加计数值
        for i in features:
            self.incf(i, cat)
            
        # 增加针对该分类的计数值
        self.incc(cat)
        
    def fprob(self, f, cat):
        if self.catCount(cat) == 0:
            return 0
        # 特征在分类中出现的总次数，除以分类中包含内容的总数
        return self.fcount(f, cat) / self.catCount(cat)
        
    def weightedprob(self, f, cat, prf, weight=1.0, ap=0.5):
        # 计算当前概率值
        basicprob = prf(f, cat)

        # 统计特征在所有分类中出现的次数
        totals = sum([self.fcount(f, c) for c in self.categories()])
    
        # 计算加权平均
        bp = ((weight * ap) + (totals * basicprob)) / (weight + totals)
        return bp


class Naivebayes(Classifier):
    def __init__(self, getfeatures):
        Classifier.__init__(self, getfeatures)
        self.thresholds = {}
        
    def setThreshold(self, cat, t):
        self.thresholds[cat] = t
        
    def getThreshold(self, cat):
        if cat not in self.thresholds:
            return 1.0
        return self.thresholds[cat]
        
    def classify(self, item, default=None):
        probs = {}
        # 查找概率最大的分类
        max = 0.0
        for cat in self.categories():
            probs[cat] = self.prob(item, cat)
            if probs[cat] > max: 
                max = probs[cat]
                best = cat

        # 确保概率值超出域值*次大概率值
        for cat in probs:
            if cat == best: 
                continue
            if probs[cat] * self.getThreshold(best) > probs[best]: 
                return default
        
        return best
    
    def docProb(self, item, cat):
        features = self.getfeatures(item)
        # 将所有特征的概率相乘
        p = 1
        for f in features:
            p *= self.weightedprob(f, cat, self.fprob)
            
        return p
    
    def prob(self, item, cat):
        catProb = self.catCount(cat) / self.totalCount()
        docProb = self.docProb(item, cat)
        return docProb * catProb
        

class FisherClassifier(Classifier):
    def __init__(self, getfeatures):
        Classifier.__init__(self, getfeatures)
        self.minimums = {}
    
    def setminimum(self, cat, min):
        self.minimums[cat] = min
  
    def getminimum(self, cat):
        if cat not in self.minimums: 
            return 0
        return self.minimums[cat]

    def cprob(self, f, cat):
        # 特征在该分类中出现的概率  
        clf = self.fprob(f, cat)
        if clf == 0: 
            return 0
    
        # 特征在所有分类中出现的概率
        freqsum = sum([self.fprob(f, c) for c in self.categories()])
    
        #  概率等于特征在该分类中出现的频率处理总体频率
        p = clf / (freqsum)
        
        return p

    
    def fisherProb(self, item, cat):
        # 将所有概率值相乘
        p = 1
        features = self.getfeatures(item)
        for f in features:
            p *= (self.weightedprob(f, cat, self.cprob))
    
        # 去自然对数，并乘以-2
        fscore = -2 * math.log(p)
    
        # 利用导致对数卡方函数求得概率
        return self.invchi2(fscore, len(features) * 2)
  
  
    def invchi2(self, chi, df):
        m = chi / 2.0
        sum = term = math.exp(-m)
        for i in range(1, df // 2):
            term *= m / i
            sum += term
        return min(sum, 1.0)

    def classify(self, item, default=None):
        # 遍历并寻找最佳结果
        best = default
        max = 0.0
        for c in self.categories():
            p = self.fisherProb(item, c)
            # 确保其查过下限值
            if p > self.getminimum(c) and p > max:
                best = c
                max = p
        return best
