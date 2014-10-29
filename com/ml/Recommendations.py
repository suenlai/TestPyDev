# coding:utf-8

# 电影评分字典
critics = {'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
 'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5,
 'The Night Listener': 3.0},
'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,
 'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0,
 'You, Me and Dupree': 3.5},
'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
 'Superman Returns': 3.5, 'The Night Listener': 4.0},
'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
 'The Night Listener': 4.5, 'Superman Returns': 4.0,
 'You, Me and Dupree': 2.5},
'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
 'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
 'You, Me and Dupree': 2.0},
'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
 'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
'Toby': {'Snakes on a Plane':4.5, 'You, Me and Dupree':1.0, 'Superman Returns':4.0}}


from math import sqrt

# 返回person1和person2的基于距离的相似度评价，用欧几里德公式
def simDistance(prefs, person1, person2):
    # sharedItems列表
    sharedItems = {}
    for item in prefs[person1]: 
        if item in prefs[person2]: 
            sharedItems[item] = 1

    # 如果2个人没有共同之处就返回
    if len(sharedItems) == 0: 
        return 0

    # 计算所有差值的平方和
    sum_of_squares = sum([pow(prefs[person1][item] - prefs[person2][item], 2) 
                      for item in prefs[person1] if item in prefs[person2]])

    return 1 / (1 + sum_of_squares)


# 返回person1和person2的皮尔逊相关系数
def simPearson(prefs, person1, person2):
    # 得到双方都评价过的物品列表
    sharedItems = {}
    for item in prefs[person1]: 
        if item in prefs[person2]: 
            sharedItems[item] = 1
    
    # 如果2个人没有共同之处就返回
    if len(sharedItems) == 0: 
        return 0
    
    # 得到列表的元素个数
    n = len(sharedItems)
      
    # 对所有偏好求和
    sum1 = sum([prefs[person1][it] for it in sharedItems])
    sum2 = sum([prefs[person2][it] for it in sharedItems])
      
    # 求平方和
    sum1Sq = sum([pow(prefs[person1][it], 2) for it in sharedItems])
    sum2Sq = sum([pow(prefs[person2][it], 2) for it in sharedItems])    
      
    # 求乘积和
    pSum = sum([prefs[person1][it] * prefs[person2][it] for it in sharedItems])
      
    # 计算皮尔逊评价值
    num = pSum - (sum1 * sum2 / n)
    den = sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n))
    
    if den == 0: 
        return 0
    
    r = num / den
    
    return r

# 从反映偏好的字典中返回最匹配者，返回结果的个数和相识度函数为可选参数
def topMatches(prefs, person, n=5, similarity=simPearson):
    scores = [(similarity(prefs, person, other), other) 
                  for other in prefs if other != person]
    
    # 对列表进行排序，评价最高的排在最前面
    scores.sort()
    scores.reverse()
    return scores[0:n]

#利用所有其他人评价值的加权平均，为某人提供推荐
def getRecommendations(prefs, person, similarity=simPearson):
    totals = {}
    simSums = {}
    for other in prefs:
        # 不和自己做比较
        if other == person: 
            continue
        sim = similarity(prefs, person, other)

        # 忽略评价值为0或小于0的情况
        if sim <= 0: 
            continue
        
        for item in prefs[other]:
            # 只对自己还未曾看过的影片进行评价
            if item not in prefs[person] or prefs[person][item] == 0:
                # 相似度 * 评价值
                totals.setdefault(item, 0)
                totals[item] += prefs[other][item] * sim
                # 相似度之和
                simSums.setdefault(item, 0)
                simSums[item] += sim

    # 建立一个归一化的列表
    rankings = [(total / simSums[item], item) for item, total in totals.items()]

    # 返回排序的列表
    rankings.sort()
    rankings.reverse()
    
    return rankings

#物品和人员对调
def transformPrefs(prefs):
    result={}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item,{})
      
            # 物品和人员对调
            result[item][person]=prefs[person][item]
            
    return result

def main():
    #simDistance(critics, 'Lisa Rose', 'Toby')
    movies = transformPrefs(critics)
    print topMatches(movies, 'Superman Returns')
    

if __name__ == '__main__':
    main()
