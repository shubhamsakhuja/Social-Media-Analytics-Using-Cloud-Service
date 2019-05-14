"""
The purpose of this code is to transfer result to sin on couchDB
result is use to show on the pie chart and sin is use to show on the bar chart
sin is the top5 sin on out result
the database name may need to be change
"""


import json
import couchdb
from collections import Counter


dic = {
	"Homicide":"Wrath",
	"Assault":"Pride",
	"Sexual":"Lust",
	"Abduction":"Wrath",
	"Robbery":"Greed",
	"Blackmail and extortion":"Greed",
	"Stalking harassment and threatening":"Wrath",
	"Negligent":"Sloth",
	"Arson":"Wrath",
	"Burglary":"Greed",
	"Theft":"Greed",
	"Deception":"Greed",
	"Bribery":"Greed",
	"Drug":"Gluttony",
	"Weapon and explosive":"Envy",
	"Disorderly":"Sloth",
	"other offence":"Wrath"
}


user = "admin"
password = "demis"
couchserver = couchdb.Server("http://%s:%s@172.26.38.21:5984/" % (user, password))

# this line indicate where the result from
db_result = couchserver["history_result"]

count = Counter()


# db_sin = couchserver.create("aurin_sin")

rows = db_result.view('_all_docs', include_docs=True)
for row in rows:
	data = row['doc']
	for i in data:
		if i == '_id' or i =='_rev':
			continue
		count[i] = data[i]

# print(count)
top5 = count.most_common(5)
# ordered = sorted(count, key=count.get, reverse=True)

topDic = {}
for (i, j) in top5:
	sin_name = dic[i]
	name = i + '-' + sin_name
	topDic[name] = j


# this lines indicate where to store the sin data
try:
	db_sin = couchserver.create("history_result")
except:
	del couchserver["history_result"]
	db_sin = couchserver.create("history_result")

db_sin.save(topDic)




