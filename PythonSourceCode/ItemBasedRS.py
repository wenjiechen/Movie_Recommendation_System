'''
Created on May 3, 2013

@author: WnejieChen
'''
import MySQLdb as db
import sys
import operator
import numpy as np
import math

MAX = sys.maxint
MIN = -MAX
# DB = 'MoiveLens10M'
# DB = 'MoiveLens1M'
DB = 'MoiveLens100K';
UNG = 6040 
ING = 3952

def executeSql(query):
    conn = db.connect(db=DB, host='localhost', user='root', passwd='1234')
    cursor = conn.cursor()
    cursor.execute(query)
    res = cursor.fetchall()
    cursor.close()
    return res
    
#run only one time to get user and item number in database
def getUserAndItemsNum():
    query = """SELECT MAX(customer_id), MAX(movie_id)
                FROM ratings"""
    res = executeSql(query)
    global UNG
    UNG = res[0][0]
    global ING
    ING = res[0][1]
    print UNG,ING    

def get2Vectors(id1,id2):
    query = """
                SELECT r1.rating, r2.rating
                FROM ratings AS r1,ratings AS r2
                WHERE r1.customer_id = r2.customer_id 
                AND r1.movie_id = %d
                AND r2.movie_id = %d;""" %(id1,id2)
    return executeSql(query)

def getitemAvgrating(mid):
    query="""
             SELECT a1.rating 
             FROM avg_ratings AS a1
             WHERE a1.movie_id = %d""" %(mid)
    return executeSql(query)

def getUserAvgRating(uid):
    query="""
            SELECT rating
            FROM user_avg_ratings
            WHERE customer_id = %d""" %uid
    return executeSql(query)

def getItemsNum(mid = ING):
    query = """
                SELECT DISTINCT movie_id
                FROM ratings
                WHERE movie_id <= %d
                """%mid
    res = executeSql(query)
    items = []
    for r in res:
        items.append(r[0])
    return items

def cosine(v1,v2):
    return np.dot(v1,v2)/(np.sqrt(np.dot(v1, v1)) * np.sqrt(np.dot(v2, v2)))

#rvs: 2 rating vectors
#avgs: average rating for two 
def pearsonCorrelation(rvs,avg1,avg2):
    if len(rvs) < 10:
        return 0    
    v1 = [i[0] for i in rvs]
    v2 = [i[1] for i in rvs]
    avg1 = np.array(avg1)
    avg2 = np.array(avg2)
    v1 -= avg1
    v2 -= avg2    
    return cosine(v1,v2)
    
def adjustCosineSimilarity(rvs,uar):
    if len(rvs) < 10:
        return 0
    v1 = [i[0] for i in rvs]
    v2 = [i[1] for i in rvs]
    uar = np.array(uar)
    v1 -= uar
    v2 -= uar
    return cosine(v1,v2)

#id: userId
#fectch items which is liked by active user 
def getActiveUserItems(userId):
    query = """SELECT movie_id,rating
                FROM ratings WHERE customer_id = %d""" %(userId)
    items = executeSql(query)
    tmp = {}
    for i in items:
        tmp[i[0]] = i[1]
    sortedItems = sorted(tmp.iteritems(),key = operator.itemgetter(1),reverse = True)
    return sortedItems

#id: item id
#rNum: number of best match items for a specific item
#itn: items Num in database
def findNBestMatchItemsForOneItem(itemId,uid,similarity = 'p',itn = ING, rNum = 10):
    sims = {}           
    avg1 = getitemAvgrating(itemId)
    uar = getUserAvgRating(uid)
    for id2 in range(1,itn+1):
        if id2 == itemId:
            continue
        if id2 % 500 == 0:
            print id2
        ratingVectors = get2Vectors(itemId,id2)
        if not ratingVectors:  #check empty list
            continue
        if similarity == 'p':
            avg2 = getitemAvgrating(id2)
            sim = pearsonCorrelation(ratingVectors,avg1[0][0],avg2[0][0])
        elif similarity == 'a':
            sim = adjustCosineSimilarity(ratingVectors,uar[0][0])
        sims[id2] = sim
    sortedRetDic = sorted(sims.iteritems(),key = operator.itemgetter(1),reverse = True)
    returnItems = [sortedRetDic[j] for j in range(0,rNum)]
    print returnItems
    return returnItems 
                  
#userItemsDic : user items dictionary
def predictScoreForOneItem(mid, uid, userItemsDic, similarity = 'p'):
#     if mid in userItemsDic:
#         print 'movie %d has commended by user %d' %(mid,uid)
#         return
    avg1 = getitemAvgrating(mid)
    uar = getUserAvgRating(uid)
    sigmaPre = 0
    sigmaSim = 0
    for it in userItemsDic:
        rvs = get2Vectors(mid,it[0])
        if not rvs:  #check empty list
            continue
        if similarity == 'p':
            avg2 = getitemAvgrating(it[0])
            sim = pearsonCorrelation(rvs,avg1[0][0],avg2[0][0])
        elif similarity == 'a':
            sim = adjustCosineSimilarity(rvs,uar[0][0])
        sigmaPre += sim*it[1]
        sigmaSim += math.fabs(sim)
    if sigmaSim == 0:
        return 0
    prediction = sigmaPre/sigmaSim
    return prediction

def predicitScoresForOneUser(uid,mids,similarity = 'p'):
    userItemsDic = getActiveUserItems(uid)
#     print 'userItemsDic',userItemsDic
    predictions = {}
    for mid in mids:
        predictions[mid] = predictScoreForOneItem(mid,uid,userItemsDic,similarity)
    return predictions
          
def test():
    items = getItemsNum()
    predictions = predicitScoresForOneUser(1,items,'p')     
    print 'predictions',predictions

def main():
#     test()
    movies = getActiveUserItems(10);
    print movies;

if __name__ == '__main__':
    main()