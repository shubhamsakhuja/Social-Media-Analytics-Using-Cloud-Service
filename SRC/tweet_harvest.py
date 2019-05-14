"""
the purpose of this code is harvest tweets from internet and aimple analyze it
We use tweepy.Cursor to catch tweets, and use geocode to filter tweet to make sure tweet is from Melbourne
I will use a id_llist to avoid catch the same tweets
I will use count to count how many tweet is related to my keywords while catch it

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
try:
	user = "admin"
	password = "demis"
	couchserver = couchdb.Server("http://%s:%s@172.26.38.21:5984/" % (user, password))
except:
	print("connect to couchDB fail!!")

# open three database, if there are not, create it
try:
	db = couchserver["cluster_project"]
except:
	db = couchserver.create("cluster_project")

try:
	id_db = couchserver["id_list"]
except:
	id_db = couchserver.create("id_list")

try:
	count_db = couchserver["count"]
except:
	count_db = couchserver.create("count")


# this id list stores all ids has been catched,
# we can use this list to check if one tweet has been catched
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

count = Counter()



# this function is use to analyze the text on the tweets
# if one tweet contains one keywords, the count will plus one
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


# use tweepy to harvest tweets from the internet
# We use geocode to filter tweets and make sure all tweets are from Melbourne

try:
	public_tweets = tweepy.Cursor(api.search, geocode="-37.78374010522721,144.9474334716797,100km",languages='en').items(2000)
	for tweet in public_tweets:
		data = json.dumps(tweet._json)
		file1 = json.loads(data)

		id = file1['id']
		# if id is already in id_list, skip this tweet
		if id in id_list:
			continue
		db.save(file1)
		id_list.append(int(id))

		# text analyse
		analyse(file1)
except:
	print("tweets harvest wrong")



# write back the id_list
rows = id_db.view('_all_docs', include_docs=True)
for row in rows:
	dbdata = row['doc']
	dbdata['ids'] = id_list
	id_db.save(dbdata)






# write back the count
rows = count_db.view('_all_docs', include_docs=True)
for row in rows:
	db_count = row["doc"]
	for word in count:
		if word in db_count:
			db_count[word] += count[word]
		else:
			db_count[word] = count[word]

	count_db.save(db_count)














