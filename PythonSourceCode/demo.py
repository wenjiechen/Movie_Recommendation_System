'''
Created on May 4, 2013

@author: WnejieChen
'''
import MySQLdb
import operator
from numpy import *
import numpy as np

def cosine(v1,v2):
    return np.dot(v1,v2)/(np.sqrt(np.dot(v1, v1)) * np.sqrt(np.dot(v2, v2)))


def pearsonCorrelation(v1,v2,avg1,avg2):
    avg1 = np.array(avg1)
    avg2 = np.array(avg2)
    v1 -= avg1
    v2 -= avg2    
    return cosine(v1,v2)

if __name__ == '__main__':
#     rateList = np.array([[1,2],[3,4]])
#     x = np.transpose(rateList)
#     x = [1,2]
#     y = [3,4]
#     print pearsonCorrelation(x,y,1.5,2)
    ids = {}
    ids[1] = 100
    ids[2]= 200
    mid = 2
    if mid in ids:
        print 'movie %d has commended by user %d' %(mid,1)