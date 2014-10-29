# coding:utf-8
'''
Created on 2014年9月5日

@author: kevin

来源： http://baike.baidu.com/view/2579342.htm
'''
import socket
import CompareComment
import SplitComment
from com.xb.log.Logger import printLogger

if __name__ == '__main__':
    printLogger("start server!!")
    
    splitComment = SplitComment.SplitComment()
    splitComment.splitByjieba(['D:\\home\\file\\'])
    splitComment.ratio = splitComment.getRatio()
    
    CompareComment.CompareComment().judge(splitComment, '警龘察')
        
