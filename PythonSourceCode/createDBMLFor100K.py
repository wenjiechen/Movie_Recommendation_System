'''
Created on May 3, 2013

@author: WnejieChen
'''
import MySQLdb
import re
import os

userNumG = 6040 
itemNumG = 3952


def createTables():
    conn = MySQLdb.connect(host='localhost', user='root', passwd='1234')  
    cursor = conn.cursor()  
    cursor.execute(""" DROP DATABASE IF EXISTS `MoiveLens100K`""")
    cursor.execute("""CREATE DATABASE `MoiveLens100K`""")
    conn.select_db('MoiveLens100K') 

    cursor.execute("""
    CREATE TABLE `ratings` (
      `customer_id` int(6) NOT NULL DEFAULT '0',
      `movie_id` int(6) NOT NULL DEFAULT '0',
      `rating` float(2,1) NOT NULL DEFAULT '0.0',
      PRIMARY KEY  (`customer_id`,`movie_id`),
      KEY `movie_id` (`movie_id`),
      KEY `customer_id` (`customer_id`),
      KEY `rating` (`rating`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
""")
    cursor.close()
    
def createTableForAvgRating():
    conn = MySQLdb.connect(db = 'MoiveLens100K', host = 'localhost',user ='root',passwd = '1234')
    cursor = conn.cursor()
    cursor.execute(""" DROP TABLE IF EXISTS `avg_ratings`""")
    cursor.execute("""
    CREATE TABLE `avg_ratings` (
      `movie_id` int(6) NOT NULL DEFAULT '0',
      `rating` float(5,4) NOT NULL DEFAULT '0.00',
      PRIMARY KEY  (`movie_id`)
)ENGINE=MyISAM DEFAULT CHARSET=latin1;
""")
    cursor.close()

def createTableForUserAvgRating():
    conn = MySQLdb.connect(db = 'MoiveLens100K', host = 'localhost',user ='root',passwd = '1234')
    cursor = conn.cursor()
    cursor.execute(""" DROP TABLE IF EXISTS `user_avg_ratings`""")
    cursor.execute("""
    CREATE TABLE `user_avg_ratings` (
      `customer_id` int(6) NOT NULL DEFAULT '0',
      `rating` float(5,4) NOT NULL DEFAULT '0.00',
      PRIMARY KEY  (`customer_id`)
)ENGINE=MyISAM DEFAULT CHARSET=latin1;
""")
    cursor.close()

def calculateUserAvgRating():
    conn = MySQLdb.connect(db = 'MoiveLens100K', host = 'localhost',user ='root',passwd = '1234')
    cursor = conn.cursor()
    for uid in range(1,userNumG+1):
        query = """SELECT AVG(rating)
                FROM ratings
                WHERE customer_id = %d""" %uid
        cursor.execute(query)
        res = cursor.fetchall()
        if res[0][0]:  #check empty list
            avg =float (res[0][0])
            insertSql = """INSERT INTO `user_avg_ratings` (`customer_id`,`rating`)
                 VALUES (%d,%f);""" %(uid,avg)
            cursor.execute(insertSql)
#             if uid % 1000 == 0:
            print avg,uid
    cursor.close()

def userAvgratingTest():
    conn = MySQLdb.connect(db = 'MoiveLens100K', host = 'localhost',user ='root',passwd = '1234')
    cursor = conn.cursor()
    uid = 1
    query = """
            select *
            from user_avg_ratings
            where customer_id = %d""" %uid
    cursor.execute(query)
    res = cursor.fetchall()
    print res

def calculateAvgRating():
    conn = MySQLdb.connect(db = 'MoiveLens100K', host = 'localhost',user ='root',passwd = '1234')
    cursor = conn.cursor()
    for mid in range(1,itemNumG+1):
        query = """SELECT AVG(rating)
                FROM ratings
                WHERE movie_id = %d""" %mid
        cursor.execute(query)
        res = cursor.fetchall()
        if res[0][0]:  #check empty list
            avg =float (res[0][0])
            insertSql = """INSERT INTO `avg_ratings` (`movie_id`,`rating`)
                 VALUES (%d,%f);""" %(mid,avg)
            cursor.execute(insertSql)
            if mid % 1000 == 0:
                print avg,mid
    cursor.close()


#user id | item id | rating | timestamp.     
def segmentTest():
    line = '193    96    1    889124507'
    v = line.split('    ')
    print v
    
def importRatings():
    fileName = 'D:/MovieLens_dataset/ml-100k/u.data'
    conn = MySQLdb.connect(host='localhost', user='root', passwd='1234')
    cursor = conn.cursor()
    conn.select_db('MoiveLens100K') 
    f= open(fileName)
    i = 0
    for line in f:
        i +=1  
        if i % 100000 == 0:
            print 'process data in line %d' % (i)  # for logging purpose   
        line =line.strip()
        try:
            UserID, MovieID, Rating, date = line.split('\t')
            UserID = int (UserID)
            MovieID = int (MovieID)
            Rating = float(Rating)
        except ValueError:
            UserID =int(line[:-1])
        else:
            query="INSERT INTO `ratings` (`customer_id`,`movie_id`,`rating`) VALUES (%d,%d,%f);" % (UserID,MovieID,Rating)
            cursor.execute(query)      
    cursor.close()

def selectTest():
    conn = MySQLdb.connect(db='MoiveLens100K', host='localhost', user='root', passwd='1234')  
    cursor = conn.cursor()
    select = """SELECT customer_id,movie_id,rating
                FROM ratings WHERE customer_id = 1"""
    cursor.execute(select)
    result = cursor.fetchall()
    cursor.close()
    for i in range(0,len(result)):
        print result[i]
    

def exportToCSV():
    conn = MySQLdb.connect(db='MoiveLens100K', host='localhost', user='root', passwd='1234')  
    cursor = conn.cursor()
    fileName = "'D:/dataset/ml-100k/userItemRating100KTest.csv'"
    sql_select = """SELECT customer_id,movie_id,rating 
                        INTO OUTFILE %s
                        FIELDS TERMINATED BY ','
                        OPTIONALLY ENCLOSED BY '"'
                        LINES TERMINATED BY '\n'
                        FROM ratings
                        ORDER BY customer_id ASC""" %(fileName)
    print 'exporting'            
    cursor.execute(sql_select)
    print 'finish'
    cursor.close()
    
def avgRatingtest():
    conn = MySQLdb.connect(db='MoiveLens100K', host='localhost', user='root', passwd='1234')
    cursor = conn.cursor()
    query="""SELECT a1.movie_id,a1.rating,a2.movie_id,a2.rating 
             FROM avg_ratings AS a1,avg_ratings AS a2
             WHERE a1.movie_id = 10 AND a2.movie_id = 11"""
    cursor.execute(query)
    res = cursor.fetchall()
    for r in res:
        print r
        
                    
def main():
     createTables()
     importRatings()
     createTableForAvgRating()
     calculateAvgRating()
     createTableForUserAvgRating()
     calculateUserAvgRating()
#     userAvgratingTest()
#     segmentTest()
#     selectTest()
#    exportToCSV()
#     avgRatingtest()
    
if __name__ == "__main__":
    main()
                
