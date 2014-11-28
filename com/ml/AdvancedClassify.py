# coding:utf-8
'''
Created on 2014年11月24日

@author: kevin
'''
import os
from pylab import *

class matchrow:
    def __init__(self, row, allnum=False):
        if allnum:
            self.data = [float(row[i]) for i in range(len(row) - 1)]
        else:
            self.data = row[0:len(row) - 1]
        self.match = int(row[len(row) - 1])

def loadmatch(f, allnum=False):
    rows = []
    for line in file(f):
        rows.append(matchrow(line.split(','), allnum))
    return rows

def plotagematches(rows):
    xdm, ydm = [r.data[0] for r in rows if r.match == 1], \
          [r.data[1] for r in rows if r.match == 1]
    xdn, ydn = [r.data[0] for r in rows if r.match == 0], \
          [r.data[1] for r in rows if r.match == 0] 
  
    plot(xdm, ydm, 'bo')
    plot(xdn, ydn, 'b+')
  
    show()
    
# 线性分类
def lineartrain(rows):
    averages = {}
    counts = {}
    
    for row in rows:
        # 得到该坐标所属的分类
        cl = row.match
        
        averages.setdefault(cl, [0.0] * (len(row.data)))
        counts.setdefault(cl, 0)
    
        # 将该坐标计入averages中
        for i in range(len(row.data)):
            averages[cl][i] += float(row.data[i])
            
        # 记录每个分类中有多个坐标点
        counts[cl] += 1
        
    # 将总和除以计数值以求得平均值
    for cl, avg in averages.items():
        for i in range(len(avg)):
            avg[i] /= counts[cl]

    return averages

# 点积是指，针对2个向量，将第一个向量中的每个值与第2个向量中对应值相乘，
# 然后再将所得的每个乘积相加
def dotproduct(v1, v2):
    return sum([v1[i] * v2[i] for i in range(len(v1))])

def dpclassify(point, avgs):
    b = (dotproduct(avgs[1], avgs[1]) - dotproduct(avgs[0], avgs[0])) / 2
    y = dotproduct(point, avgs[0]) - dotproduct(point, avgs[1]) + b
    if y > 0: 
        return 0
    else: 
        return 1
    
def yesno(v):
    if v == 'yes': 
        return 1
    elif v == 'no': 
        return -1
    else: 
        return 0

def matchcount(interest1, interest2):
    l1 = interest1.split(':')
    l2 = interest2.split(':')
    x = 0
    for v in l1:
        if v in l2: x += 1
    return x
'''
def loadnumerical():
    os.chdir("../..")
    filePath = os.getcwd() + '\\res\\matchmaker.csv'
    oldrows=loadmatch(filePath)
    newrows=[]
    for row in oldrows:
        d=row.data
        data=[float(d[0]),yesno(d[1]),yesno(d[2]),
              float(d[5]),yesno(d[6]),yesno(d[7]),
              matchcount(d[3],d[8]),
              milesdistance(d[4],d[9]),
              row.match]
        newrows.append(matchrow(data))
    return newrows
'''

def veclength(v):
    return sum([p ** 2 for p in v])

# 径向基函数
def rbf(v1, v2, gamma=10):
    dv = [v1[i] - v2[i] for i in range(len(v1))]
    l = veclength(dv)
    return math.e ** (-gamma * l)

def main():
    os.chdir("../..")
    filePath = os.getcwd() + '\\res\\agesonly.csv'
    
    rows = loadmatch(filePath)

    avgs = lineartrain(rows)
    print dpclassify([30, 25], avgs)

    # plotagematches(rows)
if __name__ == '__main__':
    main()
