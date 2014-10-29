# coding:utf-8

'''
Created on 2014年10月15日

@author: kevin
'''
from math import sqrt
from PIL import Image, ImageDraw
from test.test_iterlen import len

def readfile(filename):
    lines = [line for line in file(filename)]
    print lines
  
    # 第一行是标题
    colnames = lines[0].strip().split('\t')[1:]
    print colnames
    rownames = []
    data = []
    for line in lines[1:]:
        p = line.strip().split('\t')
        # 每一行的第一列是行名
        rownames.append(p[0])
        # 剩余部分就是该行的数据
        data.append([float(x) for x in p[1:]])
    return rownames, colnames, data


def pearson(v1, v2):
    # 求和
    sum1 = sum(v1)
    sum2 = sum(v2)
  
    # 平方和
    sum1Sq = sum([pow(v, 2) for v in v1])
    sum2Sq = sum([pow(v, 2) for v in v2])    
  
    # 乘积之和
    pSum = sum([v1[i] * v2[i] for i in range(len(v1))])
  
    # 计算皮尔逊评价值
    num = pSum - (sum1 * sum2 / len(v1))
    den = sqrt((sum1Sq - pow(sum1, 2) / len(v1)) * (sum2Sq - pow(sum2, 2) / len(v1)))
    
    if den == 0: 
        return 0

    return 1.0 - num / den


class bicluster:
    def __init__(self, vec, left=None, right=None, distance=0.0, id=None):
        self.left = left
        self.right = right
        self.vec = vec
        self.id = id
        self.distance = distance
        
def hcluster(rows, distance=pearson):
    distances = {}
    currentclustid = -1

    # 最开始的聚类就是数据中的行
    clust = [bicluster(rows[i], id=i) for i in range(len(rows))]

    while len(clust) > 1:
        # print len(clust)
        lowestpair = (0, 1)
        closest = distance(clust[0].vec, clust[1].vec)

        # 遍历每一个配对，寻找最小距离
        for i in range(len(clust)):
            for j in range(i + 1, len(clust)):
                # 用distances来缓存距离的计算值
                if (clust[i].id, clust[j].id) not in distances:  
                    distances[(clust[i].id, clust[j].id)] = distance(clust[i].vec, clust[j].vec)

                d = distances[(clust[i].id, clust[j].id)]

                if d < closest:
                    closest = d
                    lowestpair = (i, j)

        # 计算2个聚类的平均值
        mergevec = [(clust[lowestpair[0]].vec[i] + clust[lowestpair[1]].vec[i]) / 2.0 for i in range(len(clust[0].vec))]
        # 建立新的聚类
        newcluster = bicluster(mergevec, left=clust[lowestpair[0]],
                         right=clust[lowestpair[1]],
                         distance=closest, id=currentclustid)
    
        # print newcluster.id
        # 不在原始集合中的聚类，其id为负数
        currentclustid -= 1
        del clust[lowestpair[1]]
        # print len(clust)
        del clust[lowestpair[0]]
        # print len(clust)
        clust.append(newcluster)

    return clust[0]

def printclust(clust, labels=None, n=0):
    # 建立层级布局
    for i in range(n): 
        print ' ',
    if clust.id < 0:
        # 负数标记代表是一个分支
        print '-'
    else:
        # 正数标记代表是一个叶结点
        if labels == None: 
            print clust.id
        else: 
            print labels[clust.id]

    # 打印
    if clust.left != None: 
        printclust(clust.left, labels=labels, n=n + 1)
    if clust.right != None: 
        printclust(clust.right, labels=labels, n=n + 1)
  
  
def getheight(clust):
    # 是否一个叶结点，若是，高度为1
    if clust.left == None and clust.right == None: 
        return 1
    
    # 否则，高度是每个分支的高度之和
    return getheight(clust.left) + getheight(clust.right)

def getdepth(clust):
    # 一个叶结点的距离是0.0
    if clust.left == None and clust.right == None: return 0

    # 一个枝节点的距离等于左右2侧分支中距离较大的，加上该枝节【表情】自身距离
    return max(getdepth(clust.left), getdepth(clust.right)) + clust.distance


def drawdendrogram(clust, labels, jpeg='clusters.jpg'):
    # 高度和高度
    h = getheight(clust) * 20
    w = 1200
    depth = getdepth(clust)

    # 由于宽度是固定的，需要对距离值做相应的调整
    scaling = float(w - 150) / depth

    # 新建一个白色的背景图
    img = Image.new('RGB', (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    draw.line((0, h / 2, 10, h / 2), fill=(255, 0, 0))    

    # 画第一个节点
    drawnode(draw, clust, 10, (h / 2), scaling, labels)
    img.save(jpeg, 'JPEG')

def drawnode(draw, clust, x, y, scaling, labels):
    if clust.id < 0:
        h1 = getheight(clust.left) * 20
        h2 = getheight(clust.right) * 20
        top = y - (h1 + h2) / 2
        bottom = y + (h1 + h2) / 2
        # 线长度
        ll = clust.distance * scaling
        # 聚类到其子节点的垂直线   
        draw.line((x, top + h1 / 2, x, bottom - h2 / 2), fill=(255, 0, 0))    
        
        # 链接左侧节点的水平线
        draw.line((x, top + h1 / 2, x + ll, top + h1 / 2), fill=(255, 0, 0))    
    
        # 链接右侧节点的水平线
        draw.line((x, bottom - h2 / 2, x + ll, bottom - h2 / 2), fill=(255, 0, 0))        
    
        # 调用函数绘制左右节点 
        drawnode(draw, clust.left, x + ll, top + h1 / 2, scaling, labels)
        drawnode(draw, clust.right, x + ll, bottom - h2 / 2, scaling, labels)
    else:   
        # 如果这是一个叶结点，则绘制节点标签
        draw.text((x + 5, y - 7), labels[clust.id], (0, 0, 0))


def rotateMatrix(data):
    newdata = []
    for i in range(len(data[0])):
        newrow = [data[j][i] for j in range(len(data))]
        newdata.append(newrow)
        
    print newdata
    return newdata
    
import random  
def kcluster(rows, distance=pearson, k=4):
    # 确定么个点的最大点和最小点
    ranges = [(min([row[i] for row in rows]), max([row[i] for row in rows])) 
              for i in range(len(rows[0]))]
    # print ranges
    
    # 随机创建k个中心点
    clusters = [[random.random() * (ranges[i][1] - ranges[i][0]) + ranges[i][0] 
               for i in range(len(rows[0]))] for j in range(k)]                                  
    # print clusters
    
    lastmatches = None
    for t in range(100):
        # print 'Iteration %d' % t
        bestmatches = [[] for i in range(k)] 
        # print bestmatches
    
        # 在每一行中寻找距离最近的中心点
        for j in range(len(rows)):
            row = rows[j]
            bestmatche = 0
            for i in range(k):
                d = distance(clusters[i], row)
                if d < distance(clusters[bestmatche], row):
                    bestmatche = i
            bestmatches[bestmatche].append(j)  
        print bestmatches
    
        # 如果结果与上一次相同，则整个过程结束
        if bestmatches == lastmatches:
            break
        lastmatches = bestmatches
    
        # 把中心点移到其所有成员的平均位置
        for i in range(k):
            avgs = [0.0] * len(rows[0])
            # print len(rows[0])
            if(len(bestmatches[i]) > 0):
                for rowid in bestmatches[i]:
                    for m in range(len(rows[rowid])):
                        avgs[m] += rows[rowid][m]
                
                for j in range(len(avgs)):
                    avgs[j] /= len(bestmatches[i])
                
                clusters[i] = avgs
        
    #print bestmatches        
    return bestmatches
    
def main():
    blognames, words, data = readfile('D:\\workspace\\TestPyDev\\com\\blogdata.txt')
    # clust = hcluster(data)
    # printclust(clust, labels=blognames)
    # drawdendrogram(clust, blognames, jpeg='xb.jpeg')
    
    # rdata = rotateMatrix(data)
    # wordclust = hcluster(rdata)
    # drawdendrogram(wordclust, words, jpeg='xb1.jpeg')
    
    kclust = kcluster(data, k=10)
    print [blognames[r] for r in kclust[0]]

if __name__ == '__main__':
    main()
