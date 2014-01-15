Movie_Recommendation_System
===========================

Movie Recommendation System for Project of Foundations of Machine Learning @ NYU

config python code on ubuntu

1. dataset comes from "MovieLens 100k": http://grouplens.org/datasets/movielens/
dataset file is "u.data". If the 'u.data' in github doesn't work, please download

2. install 'numpy' and 'python-mysqldb' package
	install 'numpy', you need gcc. If you don't have gcc,

	command: sudo apt-get install build-essential python-dev
	
	Use pip install 'numpy', command: sudo pip install numpy

	install 'python-mysqldb',command: sudo apt-get install python-mysqldb

3. set up 'u.data' file in DATASET_PATH and database config 'databaseConfig.py'

4. run 'ItemBasedRS.py', whose main function gives a demo() to return first 20 movies' predictions for user 1, and test() to return all moives' predictions for user 1 
