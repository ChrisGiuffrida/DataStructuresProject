#! /usr/bin/env python2.7

import tweepy
import json
from watson_developer_cloud import ToneAnalyzerV3

class LocationData(object):

	def __init__(self, tweets, lat, lon):
		self.tweets = tweets
		self.lat = lat
		self.lon = lon

	def printData(self):
		print "Tweets from " + str(self.lat) + ', ' + str(self.lon)
		print '----------------------'
		for num, tweet in enumerate(self.tweets):
			print str(num + 1) + '.)' + '\t' + tweet
			print

	def hasTweets(self):
		if not tweets:
			return False
		else:
			return True


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

#Take user inputs for API call

# Hard-coded for testing
'''
searchTerm = "comey"
LAT = 38.904722
LON = -77.016389
'''
numTweets = 100

searchTerm = raw_input("Enter a search term:        ")
LAT = raw_input("Enter a latitude:           ")
LON = raw_input("Enter a longitude:          ")
#numTweets = raw_input("Number of tweets to be displayed:  ")

#Return a JSON object of tweets from the Twitter API call that match the given search terms
tweets = api.search(q=searchTerm, count=numTweets, lang='en', geocode=str(LAT) + ',' + str(LON) + ',' + '60mi')

#Generate a list of the text from the individual statuses in the tweets object
searchResults = [ ]
for status in tweets['statuses']:
	searchResults.append(status['text'])

# Ensures there were tweets, i.e. searchResults is not empty
if (not searchResults):
	# No tweets were found.
	print ("No tweets found near {}, {}!").format(LAT, LON)

else:
	#Instantiate a LocationData class to store all the tweets from a given location
	current_location = LocationData(searchResults, LAT, LON)

	#Print the tweets for the given location
	current_location.printData()

	#Instantiate a ToneAnalyzer object using the Watson Developer Cloud Library
	watsonToneDetector = ToneAnalyzerV3(
	    username='c8fe8d6c-48aa-45cc-8a45-068f253f5fb6',
	    password='fOltvpcxG1Tw',
	    version='2017-02-03')

<<<<<<< HEAD
	#Print the tone information for the first tweet

	# Ensures there are tweets to be analyzed (This is redundant right now but
	# 		might be useful later).
	if (location1.hasTweets):
		print(json.dumps(
			watsonToneDetector.tone(
				text=location1.tweets[0],
				sentences=False),
			indent=4))
		watResults = watsonToneDetector.tone(
			text=location1.tweets[0],
			sentences=False)
		
		for tone_category in watResults["document_tone"]["tone_categories"]:
			for tone in tone_category["tones"]:
				print ("{}: {}").format(tone["tone_name"],tone["score"])
=======
	# Print the tone information for the first tweet
	watResults = watsonToneDetector.tone(
		text=current_location.tweets[0],
		sentences=False,
		tones="emotion")
	for tone_category in watResults["document_tone"]["tone_categories"]:
		for tone in tone_category["tones"]:
			print ("{}: {}").format(tone["tone_name"],tone["score"])
>>>>>>> a50b62cce2c9a78e12aa88fc1c8617d63653748b
