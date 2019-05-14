"""
the puepose of this code is to read the aurin data from couchDB and translate it to result
I will filter the useful information from aurin dataset and transfer it to standard format on our system

"""


import json
import couchdb
from collections import Counter



user = "admin"
password = "demis"
couchserver = couchdb.Server("http://%s:%s@172.26.38.21:5984/" % (user, password))

try:
	db = couchserver["aurin"]
	db_result = couchserver["aurin_result"]
except:
	print("cant not open the database")

count = Counter()

def countNumber(data):
	print("onece come")
	global count
	A10 = "A10 Homicide and related offence"
	A20 = "A20 Assault and related offences"
	A30 = "A30 Sexual offences"
	A40 = "A40 Abduction and related ofences"
	A50 = "A50 Robbery"
	A60 = "A60 Blackmail and extortion"
	A70 = "A70 Stalking, harassment and threatening behaviour"
	A80 = "A80 Dangerous and negligent acts endangering people"

	B10 = "B10 Arson"
	B20 = "B20 Property Damage"
	B30 = "B30 Burglary/Break and enter"
	B40 = "B40 Theft"
	B50 = "B50 Deception"
	B60 = "B60 Bribery"

	C10 = "C10 Drug dealing and trafficking"
	C20 = "C20 Cultivate or manufacture drugs"
	C30 = "C30 Drug use and possesion"
	C90 = "C90 Other drug offences"

	D10 = "D10 Weapons and explosives offence"
	D20 = "D20 Disorderly and offensive conduct"
	D30 = "D30 Public nuisance offences"
	D40 = "D40 Public security offences"

	E10 = "E10 Justice procedures"
	E20 = "E20 Breaches of orders"

	F10 = "F10 Regulatory driving offences"
	F20 = "F20 Transport regulation offences"
	F30 = "F30 Other government regulatory off"
	F90 = "F90 Miscellaneous offences"

	count["Homicide"] += data[A10]
	count["Assault"] += data[A20]
	count["Sexual"] += data[A30]
	count["Abduction"] += data[A40]
	count["Robbery"] += data[A50]
	count["Blackmail and extortion"] += data[A60]
	count["Stalking harassment and threatening"] += data[A70]
	count["Negligent"] += data[A80]

	count["Arson"] += data[B10]
	count["Burglary"] += data[B30]
	count["Theft"] += data[B40]
	count["Deception"] += data[B50]
	count["Bribery"] += data[B60]

	count["Drug"] += data[C10]
	count["Drug"] += data[C20]
	count["Drug"] += data[C30]
	count["Drug"] += data[C90]

	count["Weapon and explosive"] += data[D10]
	count["Disorderly"] += data[D20]

	# I am not sure about this other offence
	count["other offence"] += data[F90]



rows = db.view('_all_docs', include_docs=True)
for row in rows:
	data = row['doc']
	if data['LGA Name'] == "Melbourne (C)":
		countNumber(data)


print(count)

db_result.save(count)



