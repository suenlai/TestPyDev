# coding:utf-8
'''
Created on 2015年1月7日

@author: Administrator
'''
from numpy import *

def loadDataSet(fileName):
    dataMat = []                
    fr = open(fileName)
    for line in fr.readlines():
        curLine = line.strip().split('\t')
        fltLine = map(float,curLine) #转型成float
        dataMat.append(fltLine)
    return dataMat

def distEclud(vecA, vecB):
    return sqrt(sum(power(vecA - vecB, 2))) #la.norm(vecA-vecB)

def randCent(dataSet, k):
    n = shape(dataSet)[1]
    centroids = mat(zeros((k,n)))
    for j in range(n):
        minJ = min(dataSet[:,j]) 
        rangeJ = float(max(dataSet[:,j]) - minJ)
        randomMat = random.rand(k,1) #生成2行1列随机数组
        temp = mat(minJ + rangeJ * randomMat)
        centroids[:,j] = temp
        
    return centroids

def kMeans(dataSet, k, distMeas=distEclud, createCent=randCent):
    m = shape(dataSet)[0]
    clusterAssment = mat(zeros((m,2)))

    centroids = createCent(dataSet, k)
    clusterChanged = True
    while clusterChanged:
        clusterChanged = False
        for i in range(m):
            minDist = inf; minIndex = -1
            for j in range(k):#将dataSet中的没有行和centroids中的每行比较，取距离最短的一个
                distJI = distMeas(centroids[j,:],dataSet[i,:])
                if distJI < minDist:
                    minDist = distJI; minIndex = j #把距离最短的一个 的值和索引赋值
                    
            if clusterAssment[i,0] != minIndex: 
                clusterChanged = True
                
            clusterAssment[i,:] = minIndex,minDist**2
        print centroids
        for cent in range(k):#recalculate centroids
            ptsInClust = dataSet[nonzero(clusterAssment[:,0].A==cent)[0]]#get all the point in this cluster
            centroids[cent,:] = mean(ptsInClust, axis=0) #assign centroid to mean 
    return centroids, clusterAssment

def biKMeans(dataSet, k, distMeas=distEclud):
    m = shape(dataSet)[0]
    clusterAssment = mat(zeros((m, 2)))
    centroid = mean(dataSet, axis=0).tolist()[0]
    centList = [centroid]
    for j in range(m):
        dataSetTemp = dataSet[j, :]
        clusterAssment[j, 1] = distMeas(mat(centroid), dataSetTemp)**2
    
    while (len(centList) < k):
        lowestSSE = inf
        for i in range(len(centList)):
            ptsInCurrCluster = dataSet[nonzero(clusterAssment[:,0].A == i)[0],:]
            centroidMat, splitClustAss = kMeans(ptsInCurrCluster, 2, distMeas)
            sseSplit = sum(splitClustAss[:, 1])
            sseNotSplit = sum(clusterAssment[nonzero(clusterAssment[:,0].A != i)[0], 1])
            print "sseSplit, and notSplit: " , sseSplit, sseNotSplit
            
            if (sseSplit + sseNotSplit) < lowestSSE:
                bestCentToSplit = i
                bestNewCents = centroidMat
                bestClustAss = splitClustAss.copy()
                lowestSSE = sseSplit + sseNotSplit

        #print bestClustAss
        bestClustAss[nonzero(bestClustAss[:,0].A == 1)[0],0] = len(centList) #change 1 to 3,4, or whatever
        bestClustAss[nonzero(bestClustAss[:,0].A == 0)[0],0] = bestCentToSplit
        #print bestClustAss
        print 'the bestCentToSplit is: ',bestCentToSplit
        print 'the len of bestClustAss is: ', len(bestClustAss)
        centList[bestCentToSplit] = bestNewCents[0,:].tolist()[0]#replace a centroid with two best centroids 
        centList.append(bestNewCents[1,:].tolist()[0])
        clusterAssment[nonzero(clusterAssment[:,0].A == bestCentToSplit)[0],:]= bestClustAss#reassign new clusters, and SSE
        
    return mat(centList), clusterAssment
    
def main():
    import os
    filePath = os.getcwd() + '\\res\\testSet2.txt'
    dataMat = mat(loadDataSet(filePath))
    #print dataMat
    #print dataMat[:, 0]
    #print randCent(dataMat, 2)
    #print distEclud(dataMat[0], dataMat[1])
    #kMeans(dataMat, 4)
    biKMeans(dataMat, 3)

if __name__ == '__main__':
    main()