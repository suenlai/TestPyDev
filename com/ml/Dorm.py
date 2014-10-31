# coding:utf-8
'''
Created on 2014年10月31日

@author: kevin
'''
import random
import math

# The dorms, each of which has two available spaces
dorms = ['Zeus', 'Athena', 'Hercules', 'Bacchus', 'Pluto']

# People, along with their first and second choices
prefs = [('Toby', ('Bacchus', 'Hercules')),
       ('Steve', ('Zeus', 'Pluto')),
       ('Karen', ('Athena', 'Zeus')),
       ('Sarah', ('Zeus', 'Pluto')),
       ('Dave', ('Athena', 'Bacchus')),
       ('Jeff', ('Hercules', 'Pluto')),
       ('Fred', ('Pluto', 'Athena')),
       ('Suzie', ('Bacchus', 'Hercules')),
       ('Laura', ('Bacchus', 'Hercules')),
       ('James', ('Hercules', 'Athena'))]

# [(0,9),(0,8),(0,7),(0,6),...,(0,0)]
domain = [(0, (len(dorms) * 2) - i - 1) for i in range(0, len(dorms) * 2)]

def printSolution(vec):
    slots = []
    # 为每个宿舍建2个槽
    for i in range(len(dorms)):
        slots += [i, i]
        
    # 遍历每一名学生的安置情况
    for i in range(len(vec)):
        x = int(vec[i])
        # 从剩余槽中选择
        dorm = dorms[slots[x]]
        # 输出学生及其被分配的宿舍
        print prefs[i][0] , dorm
        # 删除改槽
        del slots[x]    

# 成本函数
def dormCost(vec):
    cost = 0
    # 建立一个槽序列
    slots = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4]
    
    # 遍历每一名学生
    for i in range(len(vec)):
        x = int(vec[i])
        dorm = dorms[slots[x]]
        pref = prefs[i][1]
        # 首选成本值为0， 次选成本值为1
        if pref[0] == dorm:
            cost += 0
        elif pref[1] == dorm:
            cost += 1
        else:
            cost += 3
            
        del slots[x]
    return cost

from Optimization import randomoptimize
def main():
    # print domain
    # printSolution([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    
    s = randomoptimize(domain, dormCost)
    printSolution(s)
    
if __name__ == '__main__':
    main()
