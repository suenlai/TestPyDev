# coding:utf-8
'''
Created on 2015年3月23日

@author: kevin
'''

import base64
import MySQLdb

class Searcher:
    # 
    def __init__(self, h, p, u, pwd, dbname):
        self.con = MySQLdb.connect(
        host=h,
        port=p,
        user=u,
        passwd=pwd,
        db=dbname,
        )
        self.cur = self.con.cursor()
  
    def __del__(self):
        self.cur.close()
        self.con.close()
    
    def dbcommit(self):
        self.con.commit()
      
    def getBBSMsg(self):
        result = self.cur.execute("select msg from bbs_comment where bbs_board_id = 2")
        
        info = self.cur.fetchmany(result)
        for ii in info:
            print base64.decodestring(ii[0])
            
        print result
         
           
def main():
    demo = Searcher('58.83.130.89', 3306, 'querynew', 'query1216', 'gtgj')
    demo.getBBSMsg()
    #demo.calculatePageRank()
            
if __name__ == '__main__':
    main()