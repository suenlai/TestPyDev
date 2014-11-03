# coding:utf-8
'''
Created on 2014年11月3日

@author: Administrator
'''
import re
import math
import Classifier

def getWords(doc):
    splitter=re.compile('\\W*')
    print doc
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
    c = Classifier.Classifier(getWords)
    #c.train('the quick brown fox jumps over the lazy dog','good')
    #c.train('the quick money in the online casino','bad')
    #print c.fcount('quick', 'good')
    #print c.fcount('quick', 'bad')
    #print c.fprob('quick', 'good')
        
    sampletrain(c)
    #print c.fprob('quick', 'good')
    print c.weightedprob('money', 'good',c.fprob)

if __name__ == '__main__':
    main()