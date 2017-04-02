#! /usr/bin/env python2.7

import tweepy
import json
from Queue import Queue
from watson_developer_cloud import ToneAnalyzerV3
import tweepy
import time

global tweetsQueue
tweetsQueue = Queue()

#override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
            print status.text
            tweetsQueue.put(status.text)
            watsonCall(tweetsQueue.get())

    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False

def watsonCall(tweet):
    '''watsonResults = watsonToneDetector.tone(
        text=tweet,
        sentences=False,
        tones="emotion")'''

    print(json.dumps(
    	watsonToneDetector.tone(
    	text=tweet,
    	sentences=False,
    	tones="emotion"),
    	indent=4))

#Credentials for accessing the Twitter API
ACCESS_TOKEN = "605103879-UQBxbkGs2YWvDLsnHSWwvXTCU8Cfm3PHL9hyJap3"
ACCESS_SECRET = "OUYcvwGfQ2pHYDMcYSjQ9yDqTv3j4HrE2bPEhKfcUBB1d"
CONSUMER_KEY = "eHKgPidhrtcLeCDxCxCzm94mx"
CONSUMER_SECRET = "bbFlMLQqQiPTQpGqd35z7zd4v3ks85KdLcFFxX05E1zpBpqt16"

#Authorize Twitter API using tweepy function and credentials from above
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

#Initalize API object using authorization object auth and specify return data be in JSON format
api  = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

watsonToneDetector = ToneAnalyzerV3(
	    username='c8fe8d6c-48aa-45cc-8a45-068f253f5fb6',
	    password='fOltvpcxG1Tw',
	    version='2017-02-03')

tweets = list()

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

myStream.filter(track=['trump'], async=True)
