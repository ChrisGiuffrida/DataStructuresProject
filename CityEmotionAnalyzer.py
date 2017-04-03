#! /usr/bin/env python2.7
## Names:       Chris Giuffrida, Thomas Krill, Michael Farren, Pedro SauneroMariaca
## Class:       Data Structures CSE-20312
## Description: Pull tweets from the fifteen largest metropolitan areas in the United States and analyze their emotional content.

import tweepy
import json
import re
from watson_developer_cloud import ToneAnalyzerV3
from colour import Color


# Updates the number of tweets processed and aggregates the emotional data together for a city
def aggregate_Watson_results(watson_results, temp_emotions, num_tweets_processed):
    for sentence in watson_results['sentences_tone']:
        try:
            # Loop through the emotional tones for the given tweet and aggregate them in the temp_emotions dictionary
            for tone in sentence['tone_categories'][0]['tones']:
                emotion = tone['tone_id']
                temp_emotions[emotion] += tone['score']
            num_tweets_processed += 1
        except:
            # Ignore the occasional index error for tweets that have no emotional data generated
            pass
    return num_tweets_processed


#  Averages the emotional data for a city given
def average_city_emotions(temp_emotions, num_tweets_processed, minimum_sample_size, city):
    # Loop through the five emotions
    if num_tweets_processed > minimum_sample_size:
        for emotion in temp_emotions:
            # Average the specific emotion
            temp_emotions[emotion] /= num_tweets_processed
    else:
        for emotion in temp_emotions:
            temp_emotions[emotion] = 0

    # Set emotions dictionary in the cities JSON to the temp_emotions dict
    city['emotions'] = temp_emotions


# Determine the hex color for the city based on the emotional data that will be used for shading in the map
def determine_hex_color(city):

    # Determines the strongest emotion
    strongest_emotion = ""
    strongest_value = 0
    for emotion in city["emotions"]:
        if (city["emotions"][emotion] > strongest_value):
            strongest_value = city["emotions"][emotion]
            strongest_emotion = emotion

    # Define dictionary for base colors for each emotion
    base_hexes = {
        "anger": Color("#FF0000"),
        "disgust": Color("#00FF00"),
        "fear": Color("#CC00FF"),
        "joy": Color("#FFBF00"),
        "sadness": Color("#0000FF")
        }

    # Initializes a color variable set to the strongest emotion
    color_hex = base_hexes[strongest_emotion]

    # Desaturates the base color
    color_hex.saturation *= strongest_value
    city["strongest"] = strongest_emotion
    city["color"] = color_hex.hex


# Credentials for accessing the Twitter API
ACCESS_TOKEN = "605103879-UQBxbkGs2YWvDLsnHSWwvXTCU8Cfm3PHL9hyJap3"
ACCESS_SECRET = "OUYcvwGfQ2pHYDMcYSjQ9yDqTv3j4HrE2bPEhKfcUBB1d"
CONSUMER_KEY = "eHKgPidhrtcLeCDxCxCzm94mx"
CONSUMER_SECRET = "bbFlMLQqQiPTQpGqd35z7zd4v3ks85KdLcFFxX05E1zpBpqt16"


# Authorize Twitter API using tweepy function and credentials from above
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)


# Initalize API object using authorization object auth and specify return data be in JSON format
twitter_api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())


# Establish a JSON formatted dictionary storing intitial information on the fifteen largest metro areas in the US
cities = {'cities' : [
    {'name': 'New York City, NY', 'lat' : 40.7128, 'lon' : -74.0059},
    {'name': 'Los Angeles, CA', 'lat' : 34.0522, 'lon' : -118.2437},
    {'name': 'Chicago, IL', 'lat' : 41.8781, 'lon' : -87.6298},
    {'name': 'Dallas, TX', 'lat' : 32.7767, 'lon' : -96.7970},
    {'name': 'Houston, TX', 'lat' : 29.7604, 'lon' : -95.3698},
    {'name': 'Washington, D.C.', 'lat' : 38.9072, 'lon' : -77.0369},
    {'name': 'Philadelphia, PA', 'lat' : 39.9526, 'lon' : -75.1652},
    {'name': 'Miami, FL', 'lat' : 25.7617, 'lon' : -80.1918},
    {'name': 'Atlanta, GA', 'lat' : 33.7490, 'lon' : -84.3880},
    {'name': 'Boston, MA', 'lat' : 42.3601, 'lon' : -71.0589},
    {'name': 'San Francisco, CA', 'lat' : 37.7749,'lon' : -122.4194},
    {'name': 'Phoenix, AZ', 'lat' : 33.4484, 'lon' : -112.0740},
    {'name': 'Detroit, MI', 'lat' : 42.3314, 'lon' : -83.0458},
    {'name': 'Seattle, WA', 'lat' : 47.6062, 'lon' : -122.3321},
    {'name': 'Minneapolis, MN', 'lat' : 44.9778, 'lon' : -93.2650} ] }


# Read in user-provided search query for filtering tweets
query = raw_input("Enter a query: ")


# Loop through the fifteen major metro areas to pull and analyze tweets
for city in cities['cities']:
    print city['name']
    num_tweets = 100            # The number of tweets the Twitter API will return
    latitude = city['lat']      # The latitude of the city to be analyzed, taken from the 'cities' JSON
    longitude = city['lon']     # The longitude of the city to be analyzed, taken from the 'cities' JSON


    # Make call to the API to pull down 100 tweets matching the user-inputted query and the current city's latitude and longitude
    twitter_results = twitter_api.search(q=query, count=num_tweets, lang='en', geocode=str(latitude) + ',' + str(longitude) + ',' + '40mi')


    tweets = [ ]                 # Initialize a list to store the status text from the tweets in the twitter_results JSON
    actual_tweet_count = 0       # Initialize a count variable to count the number of tweets that are stored


    # Loop through the twitter_results JSON and extract the status to put into the tweets list
    for status in twitter_results['statuses']:
        tweets.append(status['text'])
        actual_tweet_count += 1


    statuses_first_half  = ""       # Initialize variable to store a string of the first half of the tweets recieved
    statuses_second_half = ""       # Initialize variable to store a string of the second half of the tweets recieved


    # Find indices to break up the tweets list into halves, each of which will be looped through seperately
    tweetLength1 = len(tweets) / 2
    tweetLength2 = len(tweets)


    # Loop through the first half tweets, combining them into a single string seperated by periods
    for num in range(0, tweetLength1):
        tweets[num] = re.sub('[\.*]', '', tweets[num])  # Remove periods from the middle of tweets
        tweets[num] = re.sub('[\n]', ' ', tweets[num])  # Remove new line characters from tweets
        tweets[num] = re.sub('[!]', ' ', tweets[num])   # Remove ? from middle of tweets
        tweets[num] = re.sub('[?]', ' ', tweets[num])   # Remove ! from middle of tweets
        statuses_first_half += tweets[num] + ". "       # Concatenate tweets seperated by periods into single string


    # Loop through the second half tweets, combining them into a single string seperated by periods
    for num in range(tweetLength1, tweetLength2):
        tweets[num] = re.sub('[\.*]', '', tweets[num])  # Remove periods from the middle of tweets
        tweets[num] = re.sub('[\n]', ' ', tweets[num])  # Remove new line characters from tweets
        tweets[num] = re.sub('[!]', ' ', tweets[num])   # Remove ? from middle of tweets
        tweets[num] = re.sub('[?]', ' ', tweets[num])   # Remove ! from middle of tweets
        statuses_second_half += tweets[num] + ". "      # Concatenate tweets seperated by periods into single string


    #Instantiate a ToneAnalyzer object using the Watson Developer Cloud Library
    watsonToneDetector = ToneAnalyzerV3(
    	username='c8fe8d6c-48aa-45cc-8a45-068f253f5fb6',
    	password='fOltvpcxG1Tw',
    	version='2017-02-03')


    # Initialize a dictionary to store the emotional averages for each city
    temp_emotions = {'anger' : 0, 'disgust' : 0, 'fear' : 0, 'joy' : 0, 'sadness' : 0}


    # Set the minimum number of tweets that are needed for representing a city
    minimum_sample_size = 20


    # Initialize variable to count the actual number of tweets Watson gave emotional information for
    num_tweets_processed = 0


    # Make API calls to Watson Tone Analyzer to recieve emotional information for the strings of Tweet statuses
    if actual_tweet_count > minimum_sample_size:
        watson_results1 = watsonToneDetector.tone(text=statuses_first_half, sentences=True, tones='emotion')

        # Aggregate the emotional data into the temp_emotions dictionary and return an updated number of tweets processed
        num_tweets_processed = aggregate_Watson_results(watson_results1, temp_emotions, num_tweets_processed)


    if actual_tweet_count > minimum_sample_size:
        watson_results2 = watsonToneDetector.tone(text=statuses_second_half, sentences=True, tones='emotion')

        # Aggregate the emotional data into the temp_emotions dictionary and return an updated number of tweets processed
        num_tweets_processed = aggregate_Watson_results(watson_results2, temp_emotions, num_tweets_processed)


    # Call function to average the emotional data from all of the tweets for a city
    average_city_emotions(temp_emotions, num_tweets_processed, minimum_sample_size, city)


    # Determine the hex color for the city based on the emotional data that will be used for shading in the map
    if (city['emotions']['anger'] == 0):
        # Since there weren't enough tweets, set the strongest to none and the color to grey. 
        city["strongest"] = "none"
        city["color"] = Color("grey").hex
    else:
        determine_hex_color(city)

# Print the final cities JSON to the terminal
print json.dumps(cities, indent=4)
