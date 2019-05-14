"""
The purpose of this file is to read the json file to couchDB
The result of mapreduce will be a json format, I manually capy this file to localhost
The name of json file and database may need to change

"""



import tweepy
from tweepy import Stream
from tweepy import StreamListener 
from tweepy import OAuthHandler
import json
import couchdb
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Twitter API Key 
access_token = "1655276844-Rbjk1jjqYdr5gzcEyOjcCAkYfzZ0ZP9gUzPwGUY"
access_secret = "hFll6jNnGOpHLC4Nnq96YL9nxhD5peYLe0w5dq7EYXURB"
consumer_key = "3KZFaT7v2JzvUZPq3WbQjd6l1"
consumer_secret = "827ZUNUmysKigqGYwcr2Z0PbUeoS1ZNQiCZ32Q1d2G4v44bP5K"
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)




# DB credentials
user = "admin"
password = "demis"
couchserver = couchdb.Server("http://%s:%s@172.26.38.21:5984/" % (user, password))



try:
	db = couchserver["history_tweet"]
except:
	db = couchserver.create("history_tweet")

try:
	id_db = couchserver["history_id"]
except:
	id_db = couchserver.create("history_id")



f = open('twitter.json', 'r')


line = f.readline()
line = f.readline()

id_list = []

try:
    rows = id_db.view('_all_docs', include_docs=True)
    for row in rows:
        dbdata = row['doc']
        id_list = dbdata['ids']
        #print(id_list)   
except:
	print("unable to read id_list")
	id_list = []





while line:
	line = line[:-2]
	try:
		line_data = json.loads(line)
		id = line_data["id"]

		if id not in id_list:
			db.save(line_data)
			id_list.append(id)
	except:
		print("except")
		line = f.readline()
		continue

	line = f.readline()



rows = id_db.view('_all_docs', include_docs=True)
for row in rows:
	dbdata = row['doc']
	dbdata['ids'] = id_list
	id_db.save(dbdata)







