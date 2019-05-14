"""
The purpose of this file is to remove duplicated tweets on a dataset
I use a id_list to store all the tweetId on the database
if there are twe tweets have the same tweetId , delete one
the result will be store in another database
"""



import tweepy
from tweepy import Stream
from tweepy import StreamListener 
from tweepy import OAuthHandler
import json
import couchdb
import pickle

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
db = couchserver["cluster_project"]
# id_db = couchserver["id_list"]

# rows = id_db.view('_all_docs', include_docs=True)
# for row in rows:
# 	dbdata = row['doc']
# 	id_list = dbdata['ids']


id_list = []

def readFromCouchdb():

	global id_list

	rows = db.view('_all_docs', include_docs=True)
	print("prepare done")
	for row in rows:
		try:
			data = row['doc']
			id = data['id']
			if id in id_list:
				doc_id = row['id']
				del db[doc_id]
				print("delete someting")
			else:
				id_list.append(id)
		except:
			print("something wrong")

		# if id not in id_list:
		# 	id_list.append(id)
		# else:
		# 	tweetId = row['id']


readFromCouchdb()
try:
	id_db = couchserver.create("new_id_list")
except:
	print("the new_id_list is already there")
	
dic = {}
dic['ids'] = id_list

id_db.save(dic)







# def removeDuplicate(json_str):
# 	data = json.loads(json_str)
# 	id = data['id']
# 	if id not in id_list:
# 		count += 1
# 		id_list.append(id)
# 		f.write(json_str)







