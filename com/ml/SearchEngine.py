# coding:utf-8

'''
Created on 2014年10月20日

@author: kevin
'''
import re
import urllib2
import MySQLdb
from bs4 import BeautifulSoup
from urlparse import urljoin


# 被忽略的单词列表
ignoreWords = set(['the', 'of', 'to', 'and', 'a', 'in', 'is', 'it']);
    
class Crawler:
    # 
    def __init__(self, dbname):
        self.con = MySQLdb.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='xiongbin',
        db=dbname,
        )
        self.cur = self.con.cursor()
        # self.con=sqlite.connect(dbname)
  
    def __del__(self):
        self.cur.close()
        self.con.close()

    def dbcommit(self):
        self.con.commit()
    
    # 创建数据表
    def createindextables(self): 
        self.cur.execute('create table urllist(url varchar(200))')
        self.cur.execute('create table wordlist(word varchar(200))')
        self.cur.execute('create table wordlocation(urlid varchar(200),wordid varchar(200),location varchar(200))')
        self.cur.execute('create table link(fromid  varchar(200),toid  varchar(200))')
        self.cur.execute('create table linkwords(wordid varchar(200),linkid varchar(200))')
        self.cur.execute('create index wordidx on wordlist(word)')
        self.cur.execute('create index urlidx on urllist(url)')
        self.cur.execute('create index wordurlidx on wordlocation(wordid)')
        self.cur.execute('create index urltoidx on link(toid)')
        self.cur.execute('create index urlfromidx on link(fromid)')

    
    # 为每个网页建立索引
    def addToIndex(self, url, soup):
        if self.isIndexed(url):
            return
        print 'Indexing %s' % url
        
        # 获得每个单词
        text = self.getTextOnly(soup)
        words = self.separateWords(text)
        
        # 获得URL的id
        urlid = self.getEntryid('urllist', 'url', url)
        
        # 将每个单词于该url关联
        for i in range(len(words)):
            word = words[i]
            if word in ignoreWords:
                continue
            wordid = self.getEntryid('wordlist', 'word', word)
            self.cur.execute("insert into wordlocation(urlid,wordid,location) values(%d,%d,%d)" % (urlid, wordid, i))
            self.dbcommit()
    
    # 如果url已经建立索引，返回true
    def isIndexed(self, url):
        self.cur.execute("select url from urllist where url='%s'" % url)
        cu = self.cur.fetchone()
        if cu != None:
            # 检查它是否已经被检索过了
            v = self.cur.execute("select * from wordlocation where urlid='%s'" % cu[0])
            v = self.cur.fetchone()
            if v != None:
                return True
        return False
        
    # 从一个html网页中提取文字（不带标签）
    def getTextOnly(self, soup):
        v = soup.string
        if v == None:
            c = soup.contents
            resultText = ''
            for t in c:
                subText = self.getTextOnly(t)
                resultText += subText + '\n'
            return resultText
        else:
            return v.strip()
     
    # 添加一个关联2个网页的链接 
    def addLinkref(self, urlFrom, urlTo, linkText):
        words = self.separateWords(linkText)
        fromid = self.getEntryid('urllist', 'url', urlFrom)
        toid = self.getEntryid('urllist', 'url', urlTo)
        if fromid == toid: 
            return
        self.cur.execute("insert into link(fromid,toid) values (%d,%d)" % (fromid, toid))
        self.dbcommit()
        linkid = self.cur.lastrowid
        for word in words:
            if word in ignoreWords: 
                continue
            wordid = self.getEntryid('wordlist', 'word', word)
            self.cur.execute("insert into linkwords(linkid,wordid) values (%d,%d)" % (linkid, wordid))
            self.dbcommit()
     
    # 根据任何非空白字符进行分词处理
    def separateWords(self, text):
        splitter = re.compile('\\W*')
        return [s.lower() for s in splitter.split(text) if s != '']
    
    # 用于获取条目的id，并且如果条目不存在，就将其加入到数据库
    def getEntryid(self, table, field, value, createNew=True):
        self.cur.execute("select id from %s where %s='%s'" % (table, field, value))
        res = self.cur.fetchone()
        if res == None:
            self.cur.execute("insert into %s (%s) values ('%s')" % (table, field, value))
            self.dbcommit()
            return self.cur.lastrowid
        else:
            return res[0]
   
    
    # 从一个小组网页开始进行广度优先搜索，直到某一给定的深度，期间为网页建立索引
    def crawl(self, pages, depth=2):
        for i in range(depth):
            newpages = set()
            for page in pages:
                try:
                    c = urllib2.urlopen(page)
                except:
                    print "Could not open %s" % page
                    continue
                soup = BeautifulSoup(c.read()) 
                self.addToIndex(page, soup)
                
                links = soup('a')
                for link in links:
                    if ('href' in dict(link.attrs)):
                        url = urljoin(page, link['href'])
                        if url.find("'") != -1:
                            continue
                        url = url.split('#')[0]  # 去掉位置部分
                        if url[0:4] == 'http' and not self.isIndexed(url):
                            newpages.add(url)
                        linkText = self.getTextOnly(link)
                        self.addLinkref(page, url, linkText)
                        
                # self.dbcommit()
            pages = newpages


class Searcher:
    # 
    def __init__(self, dbname):
        self.con = MySQLdb.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='xiongbin',
        db=dbname,
        )
        self.cur = self.con.cursor()
        # self.con=sqlite.connect(dbname)
  
    def __del__(self):
        self.cur.close()
        self.con.close()
    
    def dbcommit(self):
        self.con.commit()
        
    def getMatchRows(self, q):
        # 构造查询的字符串
        fieldList = 'w0.urlid'
        tableList = ''
        clauseList = ''
        wordids = []
        
        # 根据空格拆分单词
        words = q.split(' ')
        tableNumber = 0
        
        for word in words:
            # 获取单词id
            self.cur.execute("select id from wordlist where word='%s'" % word)
            wordRow = self.cur.fetchone()
            
            if wordRow != None:
                wordid = wordRow[0]
                wordids.append(wordid)
                if tableNumber > 0:
                    tableList += ','
                    clauseList += ' and '
                    clauseList += 'w%d.urlid=w%d.urlid and ' % (tableNumber - 1, tableNumber)
                fieldList += ',w%d.location' % tableNumber
                tableList += 'wordlocation w%d' % tableNumber      
                clauseList += 'w%d.wordid=%d' % (tableNumber, wordid)
                tableNumber += 1

        # 根据各个组分，建立查询
        fullquery = 'select %s from %s where %s' % (fieldList, tableList, clauseList)
        print fullquery
        ss = self.cur.execute(fullquery)
        result = self.cur.fetchone()
        # rows = []
        if result != None:
            rows = [row for row in result]    
        
        return rows, wordids   
    
    
    def getScoredList(self, rows, wordids):
        totalscores = dict([(str(row), 0) for row in rows])
    
        # 放评价函数
        weights = [(1.0, self.frequencyscore(rows)),(1.0, self.pagerankscore(rows))]
        for (weight, scores) in weights:
            for url in totalscores:
                totalscores[url] += weight * scores[url]
    
        return totalscores
    
    def getUrlName(self, id):
        self.cur.execute("select url from urllist where id=%d" % int(id))
        result = self.cur.fetchone();
        if(result != None):
            return result[0]
    
    def query(self, q):
        rows, wordids = self.getMatchRows(q)
        scores = self.getScoredList(rows, wordids)
        rankedscores = [(score, url) for (url, score) in scores.items()]
        rankedscores.sort()
        rankedscores.reverse()
        for (score, urlid) in rankedscores[0:10]:
            print '%f\t%s' % (score, self.getUrlName(urlid))
    
    # 归一化处理
    def normalizescores(self, scores, smallIsBetter=0):
        vsmall = 0.00001  # 避免被0除
        if smallIsBetter:
            minscore = min(scores.values())
            return dict([(u, float(minscore) / max(vsmall, l)) for (u, l) in scores.items()])
        else:
            maxscore = max(scores.values())
            if maxscore == 0: 
                maxscore = vsmall
            return dict([(u, float(c) / maxscore) for (u, c) in scores.items()])
  
    # 单词频度
    def frequencyscore(self, rows):
        counts = dict([(str(row), 0) for row in rows])
        for row in rows: 
            counts[str(row)] += 1
        return self.normalizescores(counts)

    # 文档位置
    def locationscore(self, rows):
        locations = dict([(str(row), 1000000) for row in rows])
        for row in rows:
            print row[0:]
            loc = sum(row[1:])
            if loc < locations[row[0]]: locations[row[0]] = loc
        
        return self.normalizescores(locations, smallIsBetter=1)

    def calculatePageRank(self, iterations=20):
        # 清楚当前PageRank表
        self.cur.execute('drop table if exists pagerank')
        self.cur.execute('create table pagerank(urlid varchar(200),score float)')

        #
        self.cur.execute('insert into pagerank select id,1.0 from urllist')
        self.dbcommit()
        
        for i in range(iterations):
            print "Iteration %d" % (i)
            self.cur.execute('select id from urllist order by id')
            urlListResult = self.cur.fetchall()
            for urlid in urlListResult:
                pr = 0.15
                
                # 循环遍历指向当前网页的所有其他网页
                v = self.cur.execute('select distinct fromid from link where toid=%d' % urlid)
                #self.dbcommit()
                if(v != 0):
                    ss = self.cur.fetchall()
                    for linker in ss:
                        # 得到链接源对应的网页的PageRank值
                        self.cur.execute('select score from pagerank where urlid=%s' % linker)
                        linkingpr = self.cur.fetchone()
                    
                        # 根据链接源，求得链接总数
                        self.cur.execute('select count(*) from link where fromid=%s' % linker)
                        linkingCount = self.cur.fetchone()
                        
                        pr += 0.85 * (linkingpr[0] / linkingCount[0])
                        
                    self.cur.execute('update pagerank set score=%f where urlid=%d' % (pr, urlid[0]))
                    self.dbcommit()
                    
    def pagerankscore(self,rows):
        pageranks = {}
        for row in rows:
            self.cur.execute('select score from pagerank where urlid=%s' % str(row))
            result = self.cur.fetchone()
            if(result != None):
                pageranks[str(row)] = result[0]
            else:
                pageranks[str(row)] = 0.0
        print pageranks.items()
        
        #pageranks=dict([(str(row),self.con.execute('select score from pagerank where urlid=%d' % str(row)).fetchone()) for row in rows])
        maxrank=max(pageranks.values())
        normalizedscores=dict([(u,float(str(l))/maxrank) for (u,l) in pageranks.items()])
        return normalizedscores
        
def main():
    pagelist = ['http://www.ali213.net/']
    #demo = Crawler('searchengine')
    #demo.crawl(pagelist)
    # demo.createindextables()
    
    demo = Searcher('searchengine')
    demo.query('webos')
    #demo.calculatePageRank()
    
if __name__ == '__main__':
    main()
