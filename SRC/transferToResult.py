"""
the purpose of this code is to transfer the output of mapreduce(stored as a json file)
to result database on the couchDB
the name of jsonfile and database should change in this file
"""

import json
import couchdb
from collections import Counter


user = "admin"
password = "demis"
couchserver = couchdb.Server("http://%s:%s@172.26.38.21:5984/" % (user, password))
print("connected")

count = Counter()

try:
	db = couchserver.create("history_result")
except:
	del couchserver["history_result"]
	db = couchserver.create("history_result")

f = open("history_result.json", "r")
data = json.load(f)

rows = data["rows"]

for row in rows:
	count[row["key"]] = row["value"]

db.save(count)



