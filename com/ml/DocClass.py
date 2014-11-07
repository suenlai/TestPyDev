# coding:utf-8
'''
Created on 2014年11月3日

@author: kevin
分类
'''
import re
import math
import Classifier

def getWords(doc):
    splitter=re.compile('\\W*')
    #print doc
    #根据非字母字符拆分
    words=[s.lower() for s in splitter.split(doc) 
          if len(s)>2 and len(s)<20]
  
    # 返回不重复的词
    return dict([(w,1) for w in words])

def sampletrain(c):
    c.train('Nobody owns the water.','good')
    c.train('the quick rabbit jumps fences','good')
    c.train('buy pharmaceuticals now','bad')
    c.train('make quick money at the online casino','bad')
    c.train('the quick brown fox jumps','good')

def main():
    #c = Classifier.Classifier(getWords)
    #c = Classifier.Naivebayes(getWords)
    c = Classifier.FisherClassifier(getWords)
    #c.train('the quick brown fox jumps over the lazy dog','good')
    #c.train('the quick money in the online casino','bad')
    #print c.fcount('quick', 'good')
    #print c.fcount('quick', 'bad')
    #print c.fprob('quick', 'good')
        
    sampletrain(c)
    #print c.fprob('quick', 'good')
    #print c.weightedprob('money', 'good',c.fprob)
    #print c.prob('quick rabbit', 'good')
    #print c.prob('quick rabbit', 'bad')
    
    #print c.classify('quick rabbit', default='unknown')
    #print c.classify('quick money', default='unknown')
    
    print c.classify('quick rabbit')
    print c.classify('quick money')
    c.setminimum('bad', 0.8)
    print c.classify('quick money')
    

if __name__ == '__main__':
    main()