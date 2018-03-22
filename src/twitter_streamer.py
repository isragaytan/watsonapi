import json
import logging
import twitter
import sys
import tweepy
import json
import rethinkdb as r

from googlesearch import search


##Set log levels for messages

root = logging.getLogger()
root.setLevel(logging.INFO)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(levelname)s : %(asctime)s :%(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)


root.info('Initializing twitter API Credentials please wait...')


class MyStreamListener(tweepy.StreamListener):

	def on_status(self,status):
		#print(status)
		print(status._json)
		#print(type(status))
		#status_list = status[0]
		#print (json.dumps(status))
		#print(status.text)
		r.table('tweets').insert(status._json).run()
		root.info('Inserted Tweet')

	def on_error(self,status_code):
		if status_code == 420:

			#Disconnect the data Stream
			return False


#Function to connect and save to the DB			
def saveDB():
	root.info('Trying to connect to DB...')
	r.connect('localhost',28015).repl()
	#r.db('test').table_create('tweets').run()
	r.table('tv_shows').insert({'name':'Star Trek'}).run()
	root.info('Connected to Rethink DB ...ready for receive data..')

saveDB()

##Set credentials
auth = tweepy.OAuthHandler('HFmZWTCUpNAJl9nB4ESNPcjaz', 'fcUKZ0Lc0TPzOvV17CJQWIEr2hOlDbcowM4C5mZjvMd3kLeaUe')
auth.set_access_token('18007817-Chuh5h0yvY7CHEIyqUc5QEpQein862lcoSppB1FUU', 'Ig82cvfdXdAqmJTKvUpJdRfSmkdUoainA4tnC85rEBHTk')

api = tweepy.API(auth,parser=tweepy.parsers.JSONParser())

my_stream_listener = MyStreamListener()
stream = tweepy.Stream(auth = api.auth, listener=my_stream_listener)
stream.filter(track=['puebla'])



#Initialize Twitter with discconnected Mode

#auth = tweepy.OAuthHandler('HFmZWTCUpNAJl9nB4ESNPcjaz', 'fcUKZ0Lc0TPzOvV17CJQWIEr2hOlDbcowM4C5mZjvMd3kLeaUe')
#auth.set_access_token('18007817-Chuh5h0yvY7CHEIyqUc5QEpQein862lcoSppB1FUU', 'Ig82cvfdXdAqmJTKvUpJdRfSmkdUoainA4tnC85rEBHTk')

#api = tweepy.API(auth)

#public_tweets = api.home_timeline()
#for tweet in public_tweets:
#    print tweet