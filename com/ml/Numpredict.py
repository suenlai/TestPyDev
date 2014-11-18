# coding:utf-8
'''
Created on 2014年11月18日

@author: kevin
'''
from random import random, randint
import math

def winePrice(rating, age):
    peak_age = rating - 50
  
    # 根据等级计算价格
    price = rating / 2
    if age > peak_age:
        # 经过"峰值年" 后续5年里其品质会变差
        price = price * (5 - (age - peak_age) / 2)
    else:
        # 价格在接近"峰值年"时会增加到原值的5倍
        price = price * (5 * ((age + 1) / peak_age))
    if price < 0: 
        price = 0
    return price


def wineset1():
    rows = []
    for i in range(300):
        # 随机生成年代和等级
        rating = random() * 50 + 50
        age = random() * 50
    
        # 得到一个参考价格
        price = winePrice(rating, age)
        
        # 增加"噪声"
        price *= (random() * 0.2 + 0.9)
    
        # 加入数据集
        rows.append({'input':(rating, age),
                     'result':price})
    return rows

def euclidean(v1, v2):
    d = 0.0
    for i in range(len(v1)):
        d += (v1[i] - v2[i]) ** 2
    return math.sqrt(d)

def getDistances(data, vec1):
    distancelist = []
  
    for i in range(len(data)):
        vec2 = data[i]['input']
        distancelist.append((euclidean(vec1, vec2), i))
  
    distancelist.sort()
    return distancelist

#K-最近邻算法
def knnEstimate(data, vec1, k=5):
    # 得到经过排序的距离值
    list = getDistances(data, vec1)
    avg = 0.0
    
    # 对前k项结果求平均
    for i in range(k):
        index = list[i][1]
        avg += data[index]['result']
        
    avg = avg / k
    return avg

# 反函数
def inverseweight(dist, num=1.0, const=0.1):
    return num / (dist + const)

# 减法函数
def subtractweight(dist, const=1.0):
    if dist > const: 
        return 0
    else: 
        return const - dist

# 高斯函数
def gaussian(dist, sigma=5.0):
    return math.e ** (-dist ** 2 / (2 * sigma ** 2))
  
#加权KNN 
def knnWeighted(data, vec1, k=5, weightf=gaussian):
    # 得到距离值
    dlist = getDistances(data, vec1)
    avg = 0.0
    totalweight = 0.0
  
    # 得到加权平均值
    for i in range(k):
        dist = dlist[i][0]
        idx = dlist[i][1]
        weight = weightf(dist)
        avg += weight * data[idx]['result']
        totalweight += weight
    if totalweight == 0: return 0
    avg = avg / totalweight
    return avg 
    
def main():
    print winePrice(99.0, 1.0)
    data = wineset1()
    print data[1]['input']
    print knnEstimate(data, (95.0, 3.0))
    print knnWeighted(data, (99.0, 5.0))

if __name__ == '__main__':
    main()
