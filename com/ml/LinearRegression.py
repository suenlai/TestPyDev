# coding:utf-8
'''
Created on 2014年12月11日

@author: Administrator
'''
import matplotlib.pyplot as plt
def regresion(x, y):
    x_average = float(sum(x)) / len(x)
    y_average = float(sum(y)) / len(y)
    
    #x_sub = map((lambda x:x - x_average), x)
    #y_sub = map((lambda x:x - y_average), y)
    
    x_sub_pow2 = map((lambda x:x**2), x)
    y_sub_pow2 = map((lambda x:x**2), y)
    
    x_y_average = map((lambda x,y:x*y), x, y)
    
    i = (float(sum(x_y_average)) / len(x)) - (x_average*y_average) 
    j = (float(sum(x_sub_pow2)) / len(x)) - (x_average**2)
    a = i / j
    b = y_average - a * x_average
    
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.plot(x, y, '*')
    plt.plot([0, 15], [0*a+b, 15*a+b])
    plt.grid()
    plt.title("{0}*x+{1}".format(a, b))
    plt.show()
    
    
def main():
    x = [1.9,2.5,3.2,3.8,4.7,5.5,5.9,7.2]
    y = [22,33,30,42,38,49,42,55]
    regresion(x, y)
    
    
if __name__ == '__main__':
    main()