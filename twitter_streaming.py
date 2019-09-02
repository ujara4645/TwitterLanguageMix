# Import the necessary package to process data in JSON format
try:
	import json
except ImportError:
	import simplejson as json

# Import the tweepy and time libraries
import tweepy
import time



# Variables that contains the user credentials to access Twitter API 
ACCESS_TOKEN = '2886354621-jXXNhdtDb3AfO4kxXjaqctmE4KtpKBCEo5XtLyD'
ACCESS_SECRET = 'Bly5AL5YpSXsKY2E7sI05M4VSJLE08iyuShAOHYAg9h4o'
CONSUMER_KEY = '2eFYDi4z2U2JCk2Nfq5P76RID'
CONSUMER_SECRET = 'iWUwyLwUiHEUHr87APqjGXdYqp5EJmRiUHrNRJXvRaMUZX6bfA'

# Setup tweepy to authenticate with Twitter credentials:
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

# Create the api to connect to twitter with your credentials
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)
#---------------------------------------------------------------------------------------------------------------------
# wait_on_rate_limit= True;  will make the api to automatically wait for rate limits to replenish
# wait_on_rate_limit_notify= True;  will make the api  to print a notification when Tweepyis waiting for rate limits to replenish
#---------------------------------------------------------------------------------------------------------------------
tweets = []
file = open('collected_tweets2.txt', 'w+')

class StreamListener(tweepy.StreamListener):
	def on_status(self, status):
		s = status._json
		tweets.append(s)

	def on_error(self, status_code):
		if status_code == 420:
			return False

stream_listener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
stream.sample(is_async=True)

# Stream tweets for x seconds and write them in json format to a file
time.sleep(20)
stream.disconnect()
tweets_length = len(tweets)
file.write(json.dumps(tweets, indent = 4))

file.close()


