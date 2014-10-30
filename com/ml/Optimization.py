# coding:utf-8
'''
Created on 2014年10月29日

@author: kevin
'''
import os
import time
import random
import math

people = [('Seymour', 'BOS'),
          ('Franny', 'DAL'),
          ('Zooey', 'CAK'),
          ('Walt', 'MIA'),
          ('Buddy', 'ORD'),
          ('Les', 'OMA')]
# 纽约的机场
destination = 'LGA'

flights = {}
os.chdir("../..")
filePath = os.getcwd() + '\\res\\schedule.txt'

for line in file(filePath):
    origin, dest, depart, arrive, price = line.strip().split(',')
    flights.setdefault((origin, dest), [])
    # 把航班详情添加到航班列表中
    flights[(origin, dest)].append((depart, arrive, int(price)))

# print flights

# 计算某个给定的时间在一天中的分钟数
def getMinutes(t):
    x = time.strptime(t, '%H:%M')
    return x[3] * 60 + x[4]
  
#打印航班表格  
def printSchedule(r):
    for d in range(len(r) / 2):
        name = people[d][0]
        origin = people[d][1]
        out = flights[(origin, destination)][r[2 * d]]
        ret = flights[(destination, origin)][r[2 * d + 1]]
        print '%10s%10s %5s-%5s $%3s %5s-%5s $%3s' % (name, origin, out[0], out[1], out[2], ret[0], ret[1], ret[2])

#成本函数
def scheduleCost(sol):
    totalprice = 0
    latestarrival = 0
    earliestdep = 24 * 60
    # 得到往返航班
    for d in range(len(sol) / 2):
        origin = people[d][1]
        outbound = flights[(origin, destination)][int(sol[d])]
        returnf = flights[(destination, origin)][int(sol[d + 1])]
    
        # 总价格等于所有往返航班之和
        totalprice += outbound[2]
        totalprice += returnf[2]
        
        # 记录最晚到达时间和最早离开时间
        if latestarrival < getMinutes(outbound[1]): 
            latestarrival = getMinutes(outbound[1])
        if earliestdep > getMinutes(returnf[0]): 
            earliestdep = getMinutes(returnf[0])
    
    # 每个人必须在机场等待知道最后一个人到达为止，
    # 他们也必须在相同时间到达，并等候返程航班
    totalwait = 0
    for d in range(len(sol) / 2):
        origin = people[d][1]
        outbound = flights[(origin, destination)][int(sol[d])]
        returnf = flights[(destination, origin)][int(sol[d + 1])]
        totalwait += latestarrival - getMinutes(outbound[1])
        totalwait += getMinutes(returnf[0]) - earliestdep
    
    # 是否多付一个的汽车租用费
    if latestarrival > earliestdep: 
        totalprice += 50
      
    return totalprice + totalwait


def main():
    # print filePath
    s = [1, 4, 3, 2, 7, 3, 6, 3, 2, 4, 5, 3]
    printSchedule(s)
    print scheduleCost(s)

if __name__ == '__main__':
    main()
