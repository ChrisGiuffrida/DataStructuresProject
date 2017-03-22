#! /usr/bin/env python2.7

import tweepy
import json
import re
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
twitter_api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

cities = {
    '01new_york_city':["New York City, NY", 40.7128, -74.0059],
    '02los_angeles':["Los Angeles, CA", 34.0522, -118.2437],
    '03chicago':["Chicago, IL", 41.8781, -87.6298],
    '04dallas':["Dallas, TX", 32.7767, -96.7970],
    '05houston':["Houston, TX", 29.7604, -95.3698],
    '06washington_dc':["Washington, D.C.", 38.9072, -77.0369],
    '07philadelphia':["Philadelphia, PA", 39.9526, -75.1652],
    '08miami':["Miami, FL", 25.7617, -80.1918],
    '09atlanta':["Atlanta, GA", 33.7490, -84.3880],
    '10boston':["Boston, MA", 42.3601, -71.0589],
    '11san_francisco':["San Francisco, CA", 37.7749, -122.4194],
    '12phoenix':["Phoenix, AZ", 33.4484, -112.0740]
}

#for city in sorted(cities):
#    print ("{}\t{}\t{}").format(cities.get(city)[0],cities.get(city)[1],cities.get(city)[2])

query = raw_input("Enter a query: ")
latitude = cities.get('01new_york_city')[1]
longitude = cities.get('01new_york_city')[2]
num_tweets = 100

tweets = twitter_api.search(q=query, count=num_tweets, lang='en', geocode=str(latitude) + ',' + str(longitude) + ',' + '60mi')


results = [ ]
for status in tweets['statuses']:
    results.append(status['text'])

counter = 1
sentence_string = ""
for line in results:
    line = re.sub('[.]', '', line)
    sentence_string += ". " + line

#Instantiate a ToneAnalyzer object using the Watson Developer Cloud Library
watsonToneDetector = ToneAnalyzerV3(
	username='c8fe8d6c-48aa-45cc-8a45-068f253f5fb6',
	password='fOltvpcxG1Tw',
	version='2017-02-03')

print(json.dumps(
    watsonToneDetector.tone(
        text=sentence_string,
        sentences=True,
        tones='emotion'),
	indent=4))


'''
wat_results = watsonToneDetector.tone(
        text=sentence_string,
        sentences=True,
        tones='emotion'),
	indent=4))

for tone_category in wat_results["document_tone"]["tone_categories"]:
    for tone in tone_category["tones"]:
        print("Overall Emotions:")
        print ("{}: {}").format(tone["tone_name"],tone["score"])
'''
