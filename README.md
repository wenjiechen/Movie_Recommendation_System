Movie Recommendation System
---
Recommender systems, which can help customers to find potential preference, have been successfully applied in e-commerce web sites, such as Amazon and Netflix.
In this lab, we implemented Collaborative Filtering using Mahout and Python respectively, and used `Movie Lens dataset` to test and training.CF algorithms calculate similarities among users and items based on users’ rating history, and recommend the top-N similar items.

Install
---
####python version on Ubuntu

* **dataset** - comes from [MovieLens](http://grouplens.org/datasets/movielens/). Dataset file is "u.data". If the 'u.data' in github doesn't work, please download

* install `numpy` and `python-mysqldb` package
	
	- install 'numpy', you need gcc. If you don't have gcc,

	- command: sudo apt-get install build-essential python-dev
	
	- Use pip install 'numpy', command: sudo pip install numpy

	install 'python-mysqldb',command: sudo apt-get install python-mysqldb

3. set up 'u.data' file in DATASET_PATH and database config 'databaseConfig.py'

4. run 'createDBMLFor100K.py' to create database 

5. run 'ItemBasedRS.py', whose main function gives a demo() to return first 20 movies' predictions for user 1, and test() to return all moives' predictions for user 1 
