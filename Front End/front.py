from flask import Flask
from flask import Markup
from flask import Flask
from flask import render_template
import couchdb

user = "admin"
password = "demis"
couchserver = couchdb.Server("http://%s:%s@172.26.38.21:5984/" % (user, password))
db = couchserver["cluster_project"]
count_db = couchserver["tweet_result"]
aurin_db = couchserver["aurin_result"]
aurin_sin = couchserver["aurin_sin"]
tweet_sin = couchserver["tweet_sin"]

label = []
value1 = []

label_au = []
value_au = []

labels_p = []
values_p = []
colors_p = ["#DEB887", "#CD853F", "#FFF8DC"]

labels_p2 = []
values_p2 = []
colors_p2 = ["#778899", "#A9A9A9", "#C0C0C0"]

rows = count_db.view('_all_docs', include_docs=True)
for row in rows:
	dbdata = row['doc']
	for key,value in dbdata.items():
		if not key.startswith('_'):
			label.append(key)
			value1.append(value)

rows_au = aurin_db.view('_all_docs', include_docs=True)
for row in rows_au:
	dbdata_au = row['doc']
	for key,value in dbdata_au.items():
		if not key.startswith('_'):
			label_au.append(key)
			value_au.append(value)

rows_au = aurin_sin.view('_all_docs', include_docs=True)
for row in rows_au:
	dbdata_au_s = row['doc']
	for key,value in dbdata_au_s.items():
		if not key.startswith('_'):
			labels_p.append(key)
			values_p.append(value)

rows_au = tweet_sin.view('_all_docs', include_docs=True)
for row in rows_au:
	dbdata_au_s = row['doc']
	for key,value in dbdata_au_s.items():
		if not key.startswith('_'):
			labels_p2.append(key)
			values_p2.append(value)


app = Flask(__name__)

@app.route("/")
def chart():
    labels = label
    values = value1
    return render_template('/front.html', values=values, labels=labels, label_au=label_au, value_au=value_au, set = zip(values_p,labels_p,colors_p), set2 = zip(values_p2,labels_p2,colors_p2))

if __name__ == "__main__":
    #app.run(host='localhost', port = 8080)
	app.run(debug = True)