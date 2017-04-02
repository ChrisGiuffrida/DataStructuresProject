#! /usr/bin/env python2.7

import tweepy
import json
from watson_developer_cloud import ToneAnalyzerV3



#Credentials for accessing the Twitter API
ACCESS_TOKEN = "605103879-UQBxbkGs2YWvDLsnHSWwvXTCU8Cfm3PHL9hyJap3"
ACCESS_SECRET = "OUYcvwGfQ2pHYDMcYSjQ9yDqTv3j4HrE2bPEhKfcUBB1d"
CONSUMER_KEY = "eHKgPidhrtcLeCDxCxCzm94mx"
CONSUMER_SECRET = "bbFlMLQqQiPTQpGqd35z7zd4v3ks85KdLcFFxX05E1zpBpqt16"

#Authorize Twitter API using tweepy function and credentials from above
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

#Initalize API object using authorization object auth and specify return data be in JSON format
twitter_API  = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

searchTerm = raw_input("Enter a search term:        ")
RADIUS = 49.79

#Return a JSON object of tweets from the Twitter API call that match the given search terms
watsonToneDetector = ToneAnalyzerV3(
        username='c8fe8d6c-48aa-45cc-8a45-068f253f5fb6',
	    password='fOltvpcxG1Tw',
	    version='2017-02-03')


count = 1
for lat in range(2000):
    #tweets = twitter_API.search(q=searchTerm, count=1, lang='en', geocode=str(lat) + ',' + str(lon) + ',' + str(RADIUS) + 'mi')
    #for status in tweets['statuses']:
    watResults = watsonToneDetector.tone(
		        text='I like dogs and cat but I hope the streaming twitter api works and yay web server',
		        sentences=False,
		        tones="emotion")
    print watResults["document_tone"]["tone_categories"][0]['tones'][0]['tone_name']
    print watResults["document_tone"]["tone_categories"][0]['tones'][0]['score']
    print count
    print
    count+=1
