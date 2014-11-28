# coding:utf-8
'''
Created on 2014年11月28日

@author: 
'''

import feedparser
import re


feedlist=[   
          'http://news.google.com/?output=rss',
          'http://feeds.salon.com/salon/news',
          'http://www.foxnews.com/xmlfeed/rss/0,4313,0,00.rss',
          'http://www.foxnews.com/xmlfeed/rss/0,4313,80,00.rss',
          'http://www.foxnews.com/xmlfeed/rss/0,4313,81,00.rss',
          'http://rss.cnn.com/rss/edition.rss',
          'http://rss.cnn.com/rss/edition_world.rss',
          'http://rss.cnn.com/rss/edition_us.rss']

def stripHTML(h):
    p = ''
    s = 0
    for c in h:
        if c == '<': s = 1
        elif c == '>':
            s = 0
            p += ' '
        elif s == 0: p += c
    return p

def separateWords(text):
    splitter = re.compile('\\W*')
    return [s.lower() for s in splitter.split(text) if len(s) > 3]


#allwords 单词在所有文章中被使用的次数
#articlewords 单词在每篇文章中出现的次数
#articletitles 文章标题列表
def getArticleWords():
    allwords = {}
    articlewords = []
    articletitles = []
    ec = 0
    
    # 遍历订阅源
    for feed in feedlist:
        f = feedparser.parse(feed)
        #print f
        
        # 遍历每篇文章
        for e in f.entries:
            # 忽略标题相同的文章
            if e.title in articletitles: 
                continue
      
            # 提取单词
            text = e.title.encode('utf8') + stripHTML(e.description.encode('utf8'))
            words = separateWords(text)
            articlewords.append({})
            articletitles.append(e.title)
            
            #在allwords和articlewords中增加针对当前单词的计数
            for word in words:
                allwords.setdefault(word, 0)
                allwords[word] += 1
                articlewords[ec].setdefault(word, 0)
                articlewords[ec][word] += 1
            ec += 1
        
    return allwords, articlewords, articletitles
            

def makeMatrix(allwords, articlewords):
    wordVec = []
    print len(allwords)
    print len(articlewords[0])
    
    '''
    dict= {}
    for i in articlewords:
        dict = articlewords[i]
        for i in dict:
            print dict[i]
    '''    

    #只考虑在超过3篇文章中出现的，但在所有文章中出现的比例小于60%
    for w, c in allwords.items():
        if c > 3 and c < len(articlewords) * 0.6:
            wordVec.append(w)
            
    #构造单词矩阵
    matrix = [[(word in f and f[word] or 0) for word in wordVec] for f in articlewords]
    
    return matrix, wordVec

def main():
    allwords, articlewords, articletitles = getArticleWords()
    wordMatrix, wordVec =  makeMatrix(allwords, articlewords)

if __name__ == '__main__':
    main()
