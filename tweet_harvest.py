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

id_list = []

# DB credentials
user = "admin"
password = "demis"
couchserver = couchdb.Server("http://%s:%s@172.26.38.21:5984/" % (user, password))
db = couchserver["cluster_project"]
id_db = couchserver["id_list"]
count_db = couchserver["count"]

try:
    rows = id_db.view('_all_docs', include_docs=True)
    for row in rows:
        dbdata = row['doc']
        id_list = dbdata['ids']
        #print(id_list)   
except:
	print("unable to read id_list")
	id_list = []

count = Counter()





def analyse(file1):
	global count

	lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()
	def lemmatize(word):
		    lemma = lemmatizer.lemmatize(word,'v')
		    if lemma == word:
		        lemma = lemmatizer.lemmatize(word,'n')
		    return lemma

	stopWords = stopwords.words("english")

	key_list = []
	key_word = ['homicide', 'assault', 'sexual', 'abduction', 'robbery', 'blackmail', 'extortion', 'stalking', 'harassment', 'threatening', 'dangerous', 'negligent', 'burglary', 'theft', 'deception', 'briery', 'drug', 'weapons', 'explosives', 'disorderly', 'offence'] 
	for token in key_word:
		if token.isalpha():
			word = token.lower()
			word = lemmatizer.lemmatize(word)
			key_list.append(word)



	text = file1['text']
	token_list = word_tokenize(text)
	word_list = []
	for token in token_list:
		if token.isalpha():
			word = token.lower()
			word = lemmatizer.lemmatize(word)
			if word not in stopWords:
				word_list.append(word)


	for word in key_list:
		if word in word_list:
			count[word] += 1



















public_tweets = tweepy.Cursor(api.search, geocode="-37.78374010522721,144.9474334716797,100km",languages='en').items(200)
for tweet in public_tweets:
	data = json.dumps(tweet._json)
	file1 = json.loads(data)
	#print(type(file1))
	#file1 = json.dumps(tweet)
	id = file1['id']
	if id in id_list:
		continue
	db.save(file1)
	id_list.append(int(id))

	# text analyse
	analyse(file1)




# write the id_list
rows = id_db.view('_all_docs', include_docs=True)
for row in rows:
	dbdata = row['doc']
	dbdata['ids'] = id_list
	id_db.save(dbdata)




# write the count
rows = count_db.view('_all_docs', include_docs=True)
for row in rows:
	db_count = row["doc"]
	print(db_count)
	for word in count:
		if word in db_count:
			db_count[word] += count[word]
		else:
			db_count[word] = count[word]

	count_db.save(db_count)
	print(db_count)













