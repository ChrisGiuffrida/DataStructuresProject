#! /usr/bin/env python2.7
## Names:       Chris Giuffrida, Thomas Krill, Michael Farren, Pedro SauneroMariaca
## Class:       Data Structures CSE-20312
## Description: test the function used to create #Emotionalyze

import CityEmotionAnalyzer
import RealTimeEmotionAnalyzer
import json

## Set Variables
tweet_count = 0
total_emotions   =  {'anger' : 0, 'disgust' : 0, 'fear' : 0, 'joy' : 0, 'sadness' : 0}
output_emotions  =  {'average_emotions' : {'anger' : 0, 'disgust' : 0, 'fear' : 0, 'joy' : 0, 'sadness' : 0,
                     'frequency_emotions' : {
                        'count' : {'anger' : 0, 'disgust' : 0, 'fear' : 0, 'joy' : 0, 'sadness' : 0},
                        'percentage' : {'anger' : 0, 'disgust' : 0, 'fear' : 0, 'joy' : 0, 'sadness' : 0} } }

## Set Test Values
watson_results = {'document_tone':
    {'tone_categories': [
        {
            'tones': [
                {
                    'score': 0.24,
                    'tone_id': 'anger',
                    'tone_name': 'Anger'
                },
                {
                    'score': 0.24,
                    'tone_id': 'disgust',
                    'tone_name': 'Disgust'
                },
                {
                    'score': 0.21,
                    'tone_id': 'fear',
                    'tone_name': 'Fear'
                },
                {
                    'score': 0.05,
                    'tone_id': 'joy',
                    'tone_name': 'Joy'
                },
                {
                    'score': 0.26,
                    'tone_id': 'sadness',
                    'tone_name': 'Sadness'
                }
            ],
            'category_id': 'emotion_tone',
            'category_name': 'Emotion Tone'
        },
        {
            'tones': [
                {
                    'score': 0.32,
                    'tone_id': 'anger',
                    'tone_name': 'Anger'
                },
                {
                    'score': 0.18,
                    'tone_id': 'disgust',
                    'tone_name': 'Disgust'
                },
                {
                    'score': 0.09,
                    'tone_id': 'fear',
                    'tone_name': 'Fear'
                },
                {
                    'score': 0.04,
                    'tone_id': 'joy',
                    'tone_name': 'Joy'
                },
                {
                    'score': 0.37,
                    'tone_id': 'sadness',
                    'tone_name': 'Sadness'
                }
            ],
            'category_id': 'emotion_tone',
            'category_name': 'Emotion Tone'
        },
        {
            'tones': [
                {
                    'score': 0.35,
                    'tone_id': 'anger',
                    'tone_name': 'Anger'
                },
                {
                    'score': 0.22,
                    'tone_id': 'Disgust',
                    'tone_name': 'Disgust'
                },
                {
                    'score': 0.15,
                    'tone_id': 'fear',
                    'tone_name': 'Fear'
                },
                {
                    'score': 0.09,
                    'tone_id': 'joy',
                    'tone_name': 'Joy'
                },
                {
                    'score': 0.21,
                    'tone_id': 'sadness',
                    'tone_name': 'Sadness'
                }
            ],
            'category_id': 'emotion_tone',
            'category_name': 'Emotion Tone'
            }
        ]
    }
}
print "Test average_emotions and frequency_emotions functions:"
print "Preset Values (in emotion score of single tweet):"
print "     1) anger = {}, disgust = {}, fear = {}, joy = {}, sadness = {}".\
format(watson_results["document_tone"]["tone_categories"][0]['tones'][0]['score'],\
watson_results['document_tone']['tone_categories'][0]['tones'][1]['score'],\
watson_results['document_tone']['tone_categories'][0]['tones'][2]['score'],\
watson_results['document_tone']['tone_categories'][0]['tones'][3]['score'],\
watson_results['document_tone']['tone_categories'][0]['tones'][4]['score'])
print "     2) anger = {}, disgust = {}, fear = {}, joy = {}, sadness = {}".\
format(watson_results["document_tone"]["tone_categories"][1]['tones'][0]['score'],\
watson_results['document_tone']['tone_categories'][1]['tones'][1]['score'],\
watson_results['document_tone']['tone_categories'][1]['tones'][2]['score'],\
watson_results['document_tone']['tone_categories'][1]['tones'][3]['score'],\
watson_results['document_tone']['tone_categories'][1]['tones'][4]['score'])
print "     3) anger = {}, disgust = {}, fear = {}, joy = {}, sadness = {}".\
format(watson_results["document_tone"]["tone_categories"][2]['tones'][0]['score'],\
watson_results['document_tone']['tone_categories'][2]['tones'][1]['score'],\
watson_results['document_tone']['tone_categories'][2]['tones'][2]['score'],\
watson_results['document_tone']['tone_categories'][2]['tones'][3]['score'],\
watson_results['document_tone']['tone_categories'][2]['tones'][4]['score'])

## Find Counts, Average, and Frequency
RealTimeEmotionAnalyzer.average_emotions(total_emotions, output_emotions, tweet_count)
frequency_emotions(watson_results, output_emotions, tweet_count)
## Output
print "Expect:"
print "         Average:     Count:     Percentage:"
print "anger:       .30          2             .67"
print "disgust:     .21          0             0.0"
print "fear:        .15          0             0.0"
print "joy:         .06          0             0.0"
print "sadness:     .28          1             .33"
print "Output:"
print "         Average:     Count:     Percentage:"
print "anger:        {}         {}              {}".format(output_emotions['average_emotions']['anger'], output_emotions['average_emotions']['frequency_emotions']['count']['anger'], ['average_emotions']['frequency_emotions']['percentage']['anger'])
print "disgust:      {}         {}              {}".format(output_emotions['average_emotions']['disgust'], output_emotions['average_emotions']['frequency_emotions']['count']['disgust'], ['average_emotions']['frequency_emotions']['percentage']['disgust'])
print "fear:         {}         {}              {}".format(output_emotions['average_emotions']['fear'], output_emotions['average_emotions']['frequency_emotions']['count']['fear'], ['average_emotions']['frequency_emotions']['percentage']['fear'])
print "joy:          {}         {}              {}".format(output_emotions['average_emotions']['joy'], output_emotions['average_emotions']['frequency_emotions']['count']['joy'], ['average_emotions']['frequency_emotions']['percentage']['joy'])
print "sadness:      {}         {}              {}".format(output_emotions['average_emotions']['sadness'], output_emotions['average_emotions']['frequency_emotions']['count']['sadness'], ['average_emotions']['frequency_emotions']['percentage']['sadness'])
print ""
print ""

## Testing CityEmotionAnalyzer
print "Testing CityEmotionAnalyzer"
# Test1
city = {"emotions": { "anger" : 0, "disgust" : 0, "fear" : 0, "joy" : 0, "sadness" : 0} }
temp_emotions = {"emotions": { "anger" : 1.0, "disgust" : 0, "fear" : 0, "joy" : 0, "sadness" : 0} }
print "Test 1: Angry City"
print "~Preset Values (emotional average for a given city)"
print "     Anger: {}".format(temp_emotions["emotions"]["anger"])
print "     Disgust: {}".format(temp_emotions["emotions"]["disgust"])
print "     Fear: {}".format(temp_emotions["emotions"]["fear"])
print "     Joy: {}".format(temp_emotions["emotions"]["Joy"])
print "     Sadness: {}".format(temp_emotions["emotions"]["sadness"])
average_city_emotions(temp_emotions, 150, 100, city)
determine_hex_color(city)
print "~Expected Strongest Emotion: Anger"
print "~Expected Hex Color: #FF0000"
print "->Output Strongest City: {}".format(city["strongest"])
print "->Output Hex Color: {}".format("color")
# Test2
city = {"emotions": { "anger" : 0, "disgust" : 0, "fear" : 0, "joy" : 0, "sadness" : 0} }
temp_emotions = {"emotions": { "anger" : 0, "disgust" : 0, "fear" : 1, "joy" : 0, "sadness" : 0} }
print "Test 2: Fearful City"
print "~Preset Values (emotional average for a given city)"
print "     Anger: {}".format(temp_emotions["emotions"]["anger"])
print "     Disgust: {}".format(temp_emotions["emotions"]["disgust"])
print "     Fear: {}".format(temp_emotions["emotions"]["fear"])
print "     Joy: {}".format(temp_emotions["emotions"]["Joy"])
print "     Sadness: {}".format(temp_emotions["emotions"]["sadness"])
average_city_emotions(temp_emotions, 150, 100, city)
determine_hex_color(city)
print "~Expected Strongest Emotion: Fear"
print "~Expected Hex Color: #CC00FF"
print "->Output Strongest City: {}".format(city["strongest"])
print "->Output Hex Color: {}".format("color")
#Test3
city = {"emotions": { "anger" : 0, "disgust" : 0, "fear" : 0, "joy" : 0, "sadness" : 0} }
temp_emotions = {"emotions": { "anger" : 0, "disgust" : 0, "fear" : 0, "joy" : 0, "sadness" : 1.0} }
print "Test 3: Sad City"
print "~Preset Values (emotional average for a given city)"
print "     Anger: {}".format(temp_emotions["emotions"]["anger"])
print "     Disgust: {}".format(temp_emotions["emotions"]["disgust"])
print "     Fear: {}".format(temp_emotions["emotions"]["fear"])
print "     Joy: {}".format(temp_emotions["emotions"]["Joy"])
print "     Sadness: {}".format(temp_emotions["emotions"]["sadness"])
average_city_emotions(temp_emotions, 150, 100, city)
determine_hex_color(city)
print "~Expected Strongest Emotion: Sadness"
print "~Expected Hex Color: #0000FF"
print "->Output Strongest City: {}".format(city["strongest"])
print "->Output Hex Color: {}".format("color")
