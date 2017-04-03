#! /usr/bin/env python2.7
## Names:       Chris Giuffrida, Thomas Krill, Michael Farren, Pedro SauneroMariaca
## Class:       Data Structures CSE-20312
## Description: Analyze emotional content of tweets in real time given a user-inputted search term.


import json
from Queue import Queue
from watson_developer_cloud import ToneAnalyzerV3
import tweepy
import time
import sys
import os


tweetsQueue = Queue()

#Override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
            tweetsQueue.put(status.text)

    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False


def watson_call(tweet, total_emotions, tweet_count):
    watson_results = watsonToneDetector.tone(
        text=tweet,
        sentences=False,
        tones="emotion")

    tweet_count = tweet_count + 1

    for tone in watson_results['document_tone']['tone_categories'][0]['tones']:
        emotion = tone['tone_id']
        total_emotions[emotion] += tone['score']

    frequency_emotions(watson_results, output_emotions, tweet_count)

    return tweet_count


def average_emotions(total_emotions, output_emotions, tweet_count):

    os.system("clear")

    print "Tweet Number: " + str(tweet_count)

    for emotion in total_emotions:
        # Average the specific emotion
        output_emotions['average_emotions'][emotion] = total_emotions[emotion] / tweet_count


def frequency_emotions(watson_results, output_emotions, tweet_count):
    
    # Determines the strongest emotion
    strongest_emotion = ""
    strongest_value = 0
    for tone in watson_results['document_tone']['tone_categories'][0]['tones']:
        if (tone['score'] > strongest_value):
            strongest_value = tone['score']
            strongest_emotion = tone['tone_id']

    output_emotions['frequency_emotions']['count'][strongest_emotion] += 1

    for emotion in output_emotions['frequency_emotions']['percentage']:
        current_count = output_emotions['frequency_emotions']['count'][emotion]
        output_emotions['frequency_emotions']['percentage'][emotion] = current_count / float(tweet_count)


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

# Read in user-provided search query for filtering tweets
query = raw_input("Enter a query: ")

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
myStream.filter(track=[query], async=True)


tweet_count      = 0
total_emotions   =  {'anger' : 0, 'disgust' : 0, 'fear' : 0, 'joy' : 0, 'sadness' : 0}

output_emotions  =  {'average_emotions' : {'anger' : 0, 'disgust' : 0, 'fear' : 0, 'joy' : 0, 'sadness' : 0}, 
                     'frequency_emotions' : {
                        'count' : {'anger' : 0, 'disgust' : 0, 'fear' : 0, 'joy' : 0, 'sadness' : 0}, 
                        'percentage' : {'anger' : 0, 'disgust' : 0, 'fear' : 0, 'joy' : 0, 'sadness' : 0} } }

while 1 == 1:
    tweet_count = watson_call(tweetsQueue.get(), total_emotions, tweet_count)
    average_emotions(total_emotions, output_emotions, tweet_count)

    print json.dumps(output_emotions, indent=4)












