'''
Created on May 3, 2013

@author: WnejieChen
'''
import MySQLdb
import re
import os

itemNumG = 10677L

def createTables():
    conn = MySQLdb.connect(host='localhost', user='root', passwd='1234')  
    cursor = conn.cursor()  
    cursor.execute(""" DROP DATABASE IF EXISTS `MoiveLens10M`""")
    cursor.execute("""CREATE DATABASE `MoiveLens10M`""")
    conn.select_db('MoiveLens10M') 

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
    conn = MySQLdb.connect(db = 'MoiveLens10M', host = 'localhost',user ='root',passwd = '1234')
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
    
def calculateAvgRating():
    conn = MySQLdb.connect(db = 'MoiveLens10M', host = 'localhost',user ='root',passwd = '1234')
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

# UserID::MovieID::Rating::Timestamp
    
def segmentTest():
    line = '1::122::5::838985046'
    v = line.split('::')
    print v

    
def importRatings():
    fileName = 'D:/dataset/ml-10M100K/ratings.dat'
    conn = MySQLdb.connect(host='localhost', user='root', passwd='1234')
    cursor = conn.cursor()
    conn.select_db('MoiveLens10M') 
    f= open(fileName)
    i = 0
    for line in f:
        i +=1  
        if i % 1000000 == 0:
            print 'process data in line %d' % (i)  # for logging purpose   
        line =line.strip()
        try:
            UserID, MovieID, Rating, date = line.split('::')
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
    conn = MySQLdb.connect(db='MoiveLens10M', host='localhost', user='root', passwd='1234')  
    cursor = conn.cursor()
    select = """SELECT customer_id,movie_id,rating
                FROM ratings WHERE customer_id = 1"""
    cursor.execute(select)
    result = cursor.fetchall()
    cursor.close()
    for i in range(0,len(result)):
        print result[i]
    

def exportToCSV():
    conn = MySQLdb.connect(db='MoiveLens10M', host='localhost', user='root', passwd='1234')  
    cursor = conn.cursor()
    fileName = "'D:/ws2/MovieRecommonder/datasetCSV/userItemRating.csv'"
    sql_select = """SELECT customer_id,movie_id,rating 
                        INTO OUTFILE %s
                        FIELDS TERMINATED BY ','
                        OPTIONALLY ENCLOSED BY '"'
                        LINES TERMINATED BY '\n'
                        FROM ratings
                        ORDER BY customer_id ASC""" %(fileName)            
    cursor.execute(sql_select)
    cursor.close()
    
def avgRatingtest():
    conn = MySQLdb.connect(db='MoiveLens10M', host='localhost', user='root', passwd='1234')
    cursor = conn.cursor()
    query="""SELECT a1.movie_id,a1.rating,a2.movie_id,a2.rating 
             FROM avg_ratings AS a1,avg_ratings AS a2
             WHERE a1.movie_id = 10 AND a2.movie_id = 11"""
    cursor.execute(query)
    res = cursor.fetchall()
    for r in res:
        print r
        
                    
def main():
#     createTables()
#     importRatings()
#     segmentTest()
#     selectTest()
#     exportToCSV()
#     createTableForAvgRating()
#     calculateAvgRating()
    avgRatingtest()
    
if __name__ == "__main__":
    main()
                
