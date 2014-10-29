# coding:utf-8
'''
Created on 2014年10月29日

@author: kevin
'''
import os
import time
import random
import math

people = [('Seymour','BOS'),
          ('Franny','DAL'),
          ('Zooey','CAK'),
          ('Walt','MIA'),
          ('Buddy','ORD'),
          ('Les','OMA')]
# 纽约的机场
destination='LGA'

flights={}
os.chdir("../..")
filePath = os.getcwd() + '\\res\\schedule.txt'

for line in file(filePath):
    origin,dest,depart,arrive,price=line.strip().split(',')
    flights.setdefault((origin,dest),[])
    #把航班详情添加到航班列表中
    flights[(origin,dest)].append((depart,arrive,int(price)))

print flights
    
def main():
    print filePath

if __name__ == '__main__':
    main()