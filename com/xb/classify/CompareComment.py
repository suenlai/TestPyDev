# coding:utf-8
'''
Created on 2014年9月5日

@author: kevin
'''

from com.xb.log.Logger import printLogger

filterChar = [';', '', ' ', ':', '.', '。', '：', '，', ' ', '!', '（', '）', '(', ')', '！', '、']

class CompareComment:

    '''
                判断接收到的评论是否为垃圾评论
    '''
    def judge(self, splitComment, comment):
        res = splitComment.splitSingleComment(comment)  # res是分词结果，为list
        for i in filterChar:
            if i in res:
                res.remove(i)# 剔除标点字符
        ratioOfWords = []  # 记录评论中每个词在垃圾评论史料库(splitComment.ratio[key][1])中出现的概率    
        for word in res:
            if word in splitComment.ratio:
                ratioOfWords.append((word, splitComment.ratio[word][1]))  # 添加(word, ratio)元祖
            else:
                splitComment.ratio[word] = [0.6, 0.4]  # 如果评论中的词是第一次出现
                # print splitComment.ratio[word]
                                                               
            ratioOfWords.append((word, 0.4))  
        
        ratioOfWords = sorted(ratioOfWords, key=lambda x:x[1], reverse=True)[:15]
        pn = 1.0 
        ppn = 1.0
        for word in ratioOfWords:
            try:
                str = word[0] + '########' + '%f' %word[1]
                printLogger(str)
            except:
                print word[0], word[1]
            pn *= word[1]
            ppn = ppn * (1.0 - word[1])
         
        trash = pn / (pn + ppn)
        printLogger(trash)
        type = ''
        if trash > 0.9:
            type = 'trash' 
        else:
            type = 'normal'
        splitComment.flush(type, res)
        return trash
        

def main():
    demo = CompareComment()
    
if __name__ == '__main__':
    main()
