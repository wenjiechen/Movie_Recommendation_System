'''
Created on May 4, 2013

@author: Zhan
'''
import MySQLdb
import operator
from numpy import *
import numpy as np

def executeQuery(select):
    conn = MySQLdb.connect(db='MoiveLens1M', host='localhost', user='root', passwd='1234')  
    cursor = conn.cursor()
    cursor.execute(select)
    result = cursor.fetchall()
    cursor.close()
    return result
   
def createRateList():
    query = """SELECT DISTINCT customer_id 
                FROM ratings"""
    result = executeQuery(query)
    rateList = []
    for i in range(0,len(result)):
        rateList.append(result[i][0])
    return rateList

def ratedMovieList2Vector(rateList,mid):
    returnVec = [0]*len(rateList)
    query = """SELECT customer_id,rating
                FROM ratings WHERE movie_id = %d"""%(mid)
    result = executeQuery(query)
    for i in range(0,len(result)):
        if result[i][0] in rateList:
            returnVec[rateList.index(result[i][0])] =result[i][1]
    return returnVec

def cosine(v1,v2):     
    return np.dot(v1, v2) / (np.sqrt(np.dot(v1, v1)) * np.sqrt(np.dot(v2, v2)))

def pearsonCorrelation(v1,v2):
    vec1 = [v1[i] for i in range(len(v1)) if v1[i]!=0 and v2[i]!=0]
    vec2 = [v2[i] for i in range(len(v2)) if v1[i]!=0 and v2[i]!=0]
    mean1 = np.mean(v1)
    mean2 = np.mean(v2)
    vec1 -=mean1
    vec2 -=mean2
    return cosine(vec1,vec2)
    

def targetMovieItemBased(ratelist,mid,count=10):
    query = """SELECT DISTINCT movie_id 
                FROM ratings"""
    result = executeQuery(query)
    returnDic = {}
    targetRateVec = ratedMovieList2Vector(ratelist,mid)
    for i in range(0,len(result)):
        if result[i][0] == mid: continue
        movieRateVec = ratedMovieList2Vector(ratelist,result[i][0])
        similarity = cosine(targetRateVec,movieRateVec)
        print result[i][0],similarity
        returnDic[result[i][0]] = similarity
    sortedRetDic = sorted(returnDic.iteritems(),key = operator.itemgetter(1),reverse = True)
    recommendMovieList =[]
    for i in range(count):
        recommendMovieList.append(sortedRetDic[i][0])
    return recommendMovieList       
                
if __name__ == '__main__':
#     print pearsonCorrelation([3,4],[3,2])
#     rateList = createRateList()
#     recommendMovieList = targetMovieItemBased(rateList,1)
#     print recommendMovieList
    res = createRateList()
    res2=ratedMovieList2Vector(res,1)
    print res2