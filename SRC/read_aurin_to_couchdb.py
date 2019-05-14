"""
The purpose of this code is to read aurin data to the couchDB
This file will read each aurin item as a file on couchDB
"""



import json
import couchdb
from collections import Counter
import pickle

# DB credentials
user = "admin"
password = "demis"
couchserver = couchdb.Server("http://%s:%s@172.26.38.21:5984/" % (user, password))

try:
	db = couchserver.create("aurin")
except:
	print("the database is already here")

count = Counter()

try:
	f = open("csvjson.json", 'r')
except:
	print("can not find file")

data = json.load(f)

for i in data:
	db.save(i)

print("done")
