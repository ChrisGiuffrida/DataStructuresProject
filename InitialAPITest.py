#! /usr/bin/env python2.7


from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream
import requests


ACCESS_TOKEN = "605103879-UQBxbkGs2YWvDLsnHSWwvXTCU8Cfm3PHL9hyJap3"
ACCESS_SECRET = "OUYcvwGfQ2pHYDMcYSjQ9yDqTv3j4HrE2bPEhKfcUBB1d"
CONSUMER_KEY = "eHKgPidhrtcLeCDxCxCzm94mx"
CONSUMER_SECRET = "bbFlMLQqQiPTQpGqd35z7zd4v3ks85KdLcFFxX05E1zpBpqt16"

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

twitter = Twitter(auth=oauth)


searchTerm = raw_input("Enter a search term:  ")
tweets = twitter.search.tweets(q='#trump', result_type='recent', lang='en', count=10, locations=-74,40,-73,41)

print tweets