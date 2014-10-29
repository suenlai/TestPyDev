# coding:utf-8
'''
Created on 2014年9月5日

@author: kevin
'''

import re
import os
import sys
import jieba
import collections


class SplitComment:
    def __init__(self):
        self.regex = re.compile(r"[\w-]+|[\x80-\xff]{3}")
        self.wordlist = {'normal': [], 'trash': []}
        self.commentdic = {'normal': {}, 'trash': {}}
        self.ratio = {}
        self.normalnum = 0  # 正常评论回复数
        self.trashnum = 0  # 垃圾评论回复数

    '''
                分别计算正常(Normal)评论回复和垃圾(Trash)评论回复中某词在其评论回复总数的比例
                类型:['normal', 'trash']
                格式:
                            我们： 1 次
                    　　你们： 1 次
        　　            他们： 1 次
                概率:
                             我们出现的概率为 0.3
                　　     你们出现的概率为 0.3
                             他们出现的概率为 0.3
                             
                返回: dic
    '''
    def getRatioByType(self, type):
        counter = collections.Counter(self.wordlist[type])
        # print counter
        dic = collections.defaultdict(list)
        for word in list(counter):
            dic[word].append(counter[word])
        # print dic
        commentcount = len(self.commentdic[type])
        # print commentcount
        if type == 'normal':
            self.normalnum = commentcount
        elif type == 'trash':
            self.trashnum = commentcount
        for key in dic:
            dic[key][0] = dic[key][0] * 1.0 / commentcount
        # print dic
        return dic
    
    '''
                计算出所有评论回复中包含某个词的比例(比如说10个评论回复中有5个包含'我们'这个词，
                那么'我们'这个词出现的频率就是50%，这个词来自所有评论回复的分词结果)
    '''
    def getRatio(self):
        dicNormalRatio = self.getRatioByType('normal')  # 单词在正常评论回复中出现的概率
        dicTrashRatio = self.getRatioByType('trash')  # 单词在垃圾评论回复中出现的概率
        dicRatio = dicNormalRatio
        for key in dicTrashRatio:
            if key in dicRatio:
                dicRatio[key].append(dicTrashRatio[key][0])
            else:
                dicRatio[key].append(0.01)  # 若某单词只出现在正常评论回复或垃圾评论回复中，假定它在没出现类型中的概率为0.01
                dicRatio[key].append(dicTrashRatio[key][0])  
        for key in dicRatio:
            if len(dicRatio[key]) == 1:
                dicRatio[key].append(0.01)
        return dicRatio

    '''
              服务器每判定一个新评论回复都会将结果加到动态数据库中
        type = 'nomal' | 'trash'
        res is [] 新评论回复的分词结果
    '''
    def flush(self, type, res):
        if type == 'normal':
            for word in res:
                if self.ratio[word][0] == 0.01:
                    self.ratio[word][0] = 1.0 / (self.normalnum + 1)
                else:
                    self.ratio[word][0] = (1 + self.ratio[word][0] * self.normalnum) / (self.normalnum + 1)
            self.normalnum += 1
        else:
            for word in res:
                if self.ratio[word][1] == 0.01:
                    self.ratio[word][1] = 1.0 / (self.trashnum + 1)
                else:
                    self.ratio[word][1] = (1 + self.ratio[word][1] * self.trashnum) / (self.trashnum + 1)
                self.trashnum += 1

    '''
                    分割单个评论回复
                    返回分词后的单词列表list
    '''
    def splitSingleComment(self, connent): 
        try:
            string = connent.decode('gbk').encode('utf-8')
        except Exception:
            string = connent
        res = list(jieba.cut(connent, cut_all=True))
        res = list(set(res))
        return res
    
    '''使用用第三方扩展库结巴中文分词进行分词'''
    def splitByjieba(self, dirs):
            try:
                for baseDir in dirs:
                    for dirt in os.listdir(baseDir):
                        d = baseDir + dirt + "\\"
                        print d
                        for fn in os.listdir(d):
                            res = []
                            fn = d + fn
                            connent = open(fn).read();
                            # connent = connent[connent.index("\n\n")::]
                            res = list(jieba.cut(connent, cut_all=True))
                            res = list(set(res))
                            self.wordlist[dirt].extend(res)
                            if fn not in self.commentdic[dirt]:  # 去重并把评论回复的分词结果存入字典
                                self.commentdic[dirt][fn] = res

                # print self.commentdic
            except:
                pass

def main():
    demo = SplitComment()
    # demo.splitByjieba(['D:\\python_tools\\commentFilter-master\\comment\\'])
    # demo.splitSingleComment("我爱北京天安门，天安门你好")
    demo.splitByjieba(['D:\\home\\file\\'])

    dicOfRatio = demo.getRatio()
    ratio = open('D:\\home\\ratio.txt', 'w')
    
    for key in dicOfRatio:
        try:
            # print key, dicOfRatio[key]
            # 必须转成gb2312才能在txt里正常显示 XD
            ratio.write(key.decode('utf-8').encode('gbk'))
            for v in dicOfRatio[key]:
                 ratio.write(' ' + str(v))
            ratio.write('\n')
        except:
            pass
    ratio.close()

    
if __name__ == '__main__':
    main()

