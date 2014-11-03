# coding:utf-8
'''
Created on 2014年11月3日

@author: Administrator
'''

class Classifier(object):
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
    
    #属于某一分类的内容项数量
    def catCount(self,cat):
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
        
    def weightedprob(self,f,cat,prf,weight=1.0,ap=0.5):
        # 计算当前概率值
        basicprob=prf(f,cat)

        # 统计特征在所有分类中出现的次数
        totals=sum([self.fcount(f,c) for c in self.categories()])
    
        # 计算加权平均
        bp=((weight*ap)+(totals*basicprob))/(weight+totals)
        return bp
