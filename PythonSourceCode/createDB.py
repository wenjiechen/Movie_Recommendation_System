'''
Created on Apr 12, 2013

@author: WnejieChen
'''
import MySQLdb
import re
import os

def createTables():
    conn = MySQLdb.connect(host='localhost', user='root', passwd='1234')  
    cursor = conn.cursor()  
    cursor.execute(""" DROP DATABASE IF EXISTS `netflix`""")
    cursor.execute("""CREATE DATABASE `netflix`""")
    conn.select_db('netflix') 

    cursor.execute("""
    CREATE TABLE `movies` (
      `id` int(5) NOT NULL DEFAULT '0',
      `year` int(4) DEFAULT '0',
      `title` varchar(255) NOT NULL DEFAULT '',
      PRIMARY KEY  (`id`)
    ) ENGINE=MyISAM DEFAULT CHARSET=latin1;

    CREATE TABLE `probe` (
      `movie_id` int(5) NOT NULL DEFAULT '0',
      `customer_id` int(6) NOT NULL DEFAULT '0',
      KEY `movie_id` (`movie_id`)
    ) ENGINE=MyISAM DEFAULT CHARSET=latin1;

    CREATE TABLE `qualifying` (
      `customer_id` int(6) NOT NULL DEFAULT '0',
      `date` date NOT NULL DEFAULT '0000-00-00',
      `movie_id` int(5) NOT NULL DEFAULT '0',
      KEY `movie_id` (`movie_id`)
    ) ENGINE=MyISAM DEFAULT CHARSET=latin1;

    CREATE TABLE `ratings` (
      `movie_id` int(5) NOT NULL DEFAULT '0',
      `customer_id` int(6) NOT NULL DEFAULT '0',
      `rating` int(1) NOT NULL DEFAULT '0',
      `date` date NOT NULL DEFAULT '0000-00-00',
      PRIMARY KEY  (`movie_id`,`customer_id`),
      KEY `date` (`date`),
      KEY `movie_id` (`movie_id`),
      KEY `customer_id` (`customer_id`),
      KEY `rating` (`rating`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
""")
    cursor.close()

def importMovie():
    f = open('D:/dataset/nf_prize_dataset/movie_titles.txt', 'rU')
    conn = MySQLdb.connect(host='localhost', user='root', passwd='1234')
    cursor = conn.cursor()
    conn.select_db('netflix') 
    
    for line in f:
        movie_id,year,movie_title = line.rstrip().split(',',2)
        movie_id =int(movie_id)
        print movie_id
        year = year!='NULL' and int(year) or 'NULL'
        movie_title= re.escape(movie_title)
        query= "INSERT INTO `movies` (`id`,`year`,`title`) VALUES (%d,%s,'%s');" % (movie_id,year,movie_title)
        cursor.execute(query)
    cursor.close()

#another approach in regex   
#      for line in f:
#        match = re.search(r'(\d+),(\d*|NULL),(.+)',line.rstrip())
#        movie_id = int(match.group(1))
#        year= match.group(2)
#        title = match.group(3).rstrip()
#        print title
#        print "%d,%s,%s "% (movie_id,year,title)
#        query= "INSERT INTO `movies` (`id`,`year`,`title`) VALUES (%d,'%s',%s);" % (movie_id,year,title )
#        cursor.execute(query)
#    cursor.close()

def importProbe():
    f = open('D:/dataset/nf_prize_dataset/probe.txt', 'rU')
    conn = MySQLdb.connect(host='localhost', user='root', passwd='1234')
    cursor = conn.cursor()
    conn.select_db('netflix') 
    
    for line in f:
        line=line.strip()
        try:
            user_id = int(line)
        except ValueError:
            movie_id = int(line[:-1])
        else:
            query= "INSERT INTO `probe` (`movie_id`,`customer_id`) VALUES (%d,%d);" % (movie_id,user_id)
            cursor.execute(query)
    cursor.close()
            
def importQualify():
    f = open('D:/dataset/nf_prize_dataset/qualifying.txt', 'rU')
    conn = MySQLdb.connect(host='localhost', user='root', passwd='1234')
    cursor = conn.cursor()
    conn.select_db('netflix') 
    
    for line in f:
        line=line.strip()
        try:
            user_id,date = line.split(',')
            user_id = int(user_id)
        except ValueError:
            movie_id = int(line[:-1])
        else:
            query= "INSERT INTO `qualifying` (`customer_id`,`date`,`movie_id`) VALUES (%d,'%s',%d);" % (user_id,date,movie_id)
            cursor.execute(query)
    cursor.close()
             

def importRatings():
    directory = 'D:/dataset/nf_prize_dataset/training_set'
    filenames = os.listdir(directory)
    for filename in filenames:
        conn = MySQLdb.connect(host='localhost', user='root', passwd='1234')
        cursor = conn.cursor()
        conn.select_db('netflix') 
        print 'process data in file %s' %(filename)#for logging purpose
        f= open(os.path.join(directory,filename))
        for line in f:
            line =line.strip()
            try:
                user_id,rate,date=line.split(',')
                user_id = int (user_id)
                rate =int(rate)
            except ValueError:
                movie_id =int(line[:-1])
            else:
                query="INSERT INTO `ratings` (`movie_id`,`customer_id`,`rating`,`date`) VALUES (%d,%d,%d,'%s');" % (movie_id,user_id,rate,date)
                cursor.execute(query)
        cursor.close()
                
            
def exportToCSV():
    conn = MySQLdb.connect(db='netflix', host='localhost', user='root', passwd='1234')  
    cursor = conn.cursor()
    fileName = "'D:/ws2/MovieRecommonderMahout/tmp/userItemRating.csv'"
    sql_select = """SELECT customer_id,movie_id,rating 
                        INTO OUTFILE %s 
                        FIELDS TERMINATED BY ','
                        OPTIONALLY ENCLOSED BY '"'
                        LINES TERMINATED BY '\n'
                        FROM ratings
                        ORDER BY customer_id ASC""" %(fileName)
                        
    cursor.execute(sql_select)
    cursor.close()
           
def main():
#     createTables()
#     importProbe()
#     importMovie()
#     importQualify()
#    importRatings()
    exportToCSV()
    
    
if __name__ == "__main__":
    main()