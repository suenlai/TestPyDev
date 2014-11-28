# coding:utf-8
'''
Created on 2014年11月25日

@author: kevin
'''
from svm import *
from svmutil import *

def main():
    svm_model.predict = lambda self, x: svm_predict([0], [x], self)[0][0]
    
    prob = svm_problem([1, -1], [[1, 0, 1], [-1, 0, -1]])

    param = svm_parameter()
    param.kernel_type = LINEAR
    param.C = 10

    m = svm_train(prob, param)
    m.predict([1,1,1])
if __name__ == '__main__':
    main()
