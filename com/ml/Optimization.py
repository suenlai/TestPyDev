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
  
# 打印航班表格  
def printSchedule(r):
    for d in range(len(r) / 2):
        name = people[d][0]
        origin = people[d][1]
        out = flights[(origin, destination)][r[2 * d]]
        ret = flights[(destination, origin)][r[2 * d + 1]]
        print '%10s%10s %5s-%5s $%3s %5s-%5s $%3s' % (name, origin, out[0], out[1], out[2], ret[0], ret[1], ret[2])

# 成本函数
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

# 随机搜索
def randomoptimize(domain, costf):
    best = 999999999
    bestr = None
    for i in range(0, 1000):
        # 创建随机解
        r = [random.randint(domain[j][0], domain[j][1]) for j in range(len(domain))]
    
        # 得到成本
        cost = costf(r)
        
        # 比较
        if cost < best:
            best = cost
            bestr = r 
    return r

# 模拟爬山法
def hillclimb(domain, costf):
    # 创建随机解
    sol = [random.randint(domain[i][0], domain[i][1])
        for i in range(len(domain))]
    # 循环
    while 1:
        # 创建相邻解的列表
        neighbors = []
    
        for i in range(len(domain)):
            # 在每个方向上相对于原值偏离一点
            if sol[i] > domain[i][0]:
                neighbors.append(sol[0:i] + [sol[i] + 1] + sol[i + 1:])
            if sol[i] < domain[i][1]:
                neighbors.append(sol[0:i] + [sol[i] - 1] + sol[i + 1:])

        # 在相邻的解中寻找最优解
        current = costf(sol)
        best = current
        for i in range(len(neighbors)):
            #print i
            cost = costf(neighbors[i])
            if cost < best:
                best = cost
                sol = neighbors[i]

        # 如果没有更好的解，则退出
        if best == current:
            break
    return sol

# 模拟退火算法
def annealingoptimize(domain, costf, T=10000.0, cool=0.95, step=1):
    # 创建随机解
    vec = [random.randint(domain[i][0], domain[i][1]) for i in range(len(domain))]
  
    while T > 0.1:
        # 选择一个索引值
        i = random.randint(0, len(domain) - 1)
    
        # 选择一个改变索引值得方向
        dir = random.randint(-step, step)
    
        # 创建一个代表题解的新列表，改变其中一个值
        vecb = vec[:]
        vecb[i] += dir
        if vecb[i] < domain[i][0]: 
            vecb[i] = domain[i][0]
        elif vecb[i] > domain[i][1]: 
            vecb[i] = domain[i][1]
    
        # 计算当前成本
        ea = costf(vec)
        eb = costf(vecb)
        p = pow(math.e, (-eb - ea) / T)
    
        # Is it better, or does it make the probability
        # cutoff?
        if (eb < ea or random.random() < p):
            vec = vecb      
    
        # 降低温度
        T = T * cool
    return vec


def main():
    # print filePath
    # s = [1, 4, 3, 2, 7, 3, 6, 3, 2, 4, 5, 3]
    # printSchedule(s)
    # print scheduleCost(s)
    domain = [(0, 9)] * len(people) * 2
    '''
    print domain
    s = randomoptimize(domain, scheduleCost)
    print s
    print scheduleCost(s)
    printSchedule(s)
    '''
    #s = hillclimb(domain, scheduleCost)
    
    s = annealingoptimize(domain, scheduleCost)
    print scheduleCost(s)
    printSchedule(s)
    
    
if __name__ == '__main__':
    main()
