import couchdb

couchserver = couchdb.Server("http://172.26.38.21:5984/_utils")

for dbname in couchserver:
    print(dbname)

print("Done")
