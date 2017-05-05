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

#*******************************************************************************
#Instantiate a ToneAnalyzer object using the Watson Developer Cloud Library
watsonToneDetector = ToneAnalyzerV3(
        username='2f7c8ba2-a973-4fdc-9bac-b17ce1353226',
        password='IgvFw1fbdVjr',
        version='2017-02-03')

tweets_queue = Queue()

tweet_count      = 0
total_emotions   =  {'anger' : 0, 'disgust' : 0, 'fear' : 0, 'joy' : 0, 'sadness' : 0}
output_emotions  =  {'average_emotions' : {'anger' : 0, 'disgust' : 0, 'fear' : 0, 'joy' : 0, 'sadness' : 0},
                     'frequency_emotions' : {
                        'count' : {'anger' : 1, 'disgust' : 1, 'fear' : 1, 'joy' : 1, 'sadness' : 1},
                        'percentage' : {'anger' : 0, 'disgust' : 0, 'fear' : 0, 'joy' : 0, 'sadness' : 0} } }


# Override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
            # Add the text of the tweets to a queue of tweets
            tweets_queue.put(status.text)

    def on_error(self, status_code):
        if status_code == 420:
            # Returning False if the data stream is disconnecting
            return False


def initialize(query = ''):
    tweet_count      = 0
    total_emotions   =  {'anger' : 0, 'disgust' : 0, 'fear' : 0, 'joy' : 0, 'sadness' : 0}
    output_emotions  =  {'average_emotions' : {'anger' : 0, 'disgust' : 0, 'fear' : 0, 'joy' : 0, 'sadness' : 0},
                         'frequency_emotions' : {
                            'count' : {'anger' : 1, 'disgust' : 1, 'fear' : 1, 'joy' : 1, 'sadness' : 1},
                            'percentage' : {'anger' : 0, 'disgust' : 0, 'fear' : 0, 'joy' : 0, 'sadness' : 0} } }


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


    # Create a my_stream_listener object and open a twitter stream using tweepy
    my_stream_listener = MyStreamListener()
    my_stream = tweepy.Stream(auth = api.auth, listener=my_stream_listener)
    my_stream.filter(track=[query], async=True)


# Make API call to Watson for the passed-in tweet
def watson_call(tweet, total_emotions, tweet_count):

    # Make API call and save results in variable containing the JSON data
    watson_results = watsonToneDetector.tone(
        text=tweet,
        sentences=False,
        tones="emotion")

    # Increment the counter for the number of tweets analyzed by Watson
    tweet_count = tweet_count + 1


    # Add to the sum of each emotion's score in the total_emotions dictionary
    for tone in watson_results['document_tone']['tone_categories'][0]['tones']:
        emotion = tone['tone_id']
        total_emotions[emotion] += tone['score']


    # Find the emotion that had the highest score for the given tweet
    frequency_emotions(watson_results, output_emotions, tweet_count)

    return tweet_count


# Find the average emotional score for each emotion for the given twitter stream
def average_emotions(total_emotions, output_emotions, tweet_count):

    # Average each of the five emotions
    for emotion in total_emotions:
        output_emotions['average_emotions'][emotion] = total_emotions[emotion] / tweet_count


# Total the number of times each emotion has had the highest emotional score for a given tweet
def frequency_emotions(watson_results, output_emotions, tweet_count):

    # Determines the strongest emotion for a given tweet
    strongest_emotion = ""
    strongest_value = 0
    for tone in watson_results['document_tone']['tone_categories'][0]['tones']:
        if (tone['score'] > strongest_value):
            strongest_value = tone['score']
            strongest_emotion = tone['tone_id']

    # Increment the count in the output_emotions dictionary for the highest-scored emotion
    output_emotions['frequency_emotions']['count'][strongest_emotion] += 1


    # Calculate the percentage frequency of each emotion being the highest-scored emotion in a tweet
    for emotion in output_emotions['frequency_emotions']['percentage']:
        current_count = output_emotions['frequency_emotions']['count'][emotion]
        output_emotions['frequency_emotions']['percentage'][emotion] = current_count / float(tweet_count)


def getStreamData():
        global tweet_count
        # Remove one tweet from queue, analyze it with watson, and add it to the averaged data
        if tweets_queue.empty() == True:
            return output_emotions
        else:
            tweet_count = watson_call(tweets_queue.get(), total_emotions, tweet_count)
            average_emotions(total_emotions, output_emotions, tweet_count)


        # Print the updated set of emotional data for the twitter stream
        return output_emotions
