
## Names:       Chris Giuffrida, Thomas Krill, Michael Farren, Pedro SauneroMariaca
## Class:       Data Structures CSE-20312
## Description: test the function used to create #Emotionalyze

import CityEmotionAnalyzer
import RealTimeEmotionAnalyzer

## Testing CityEmotionAnalyzer
print "Testing CityEmotionAnalyzer"
# Test1
city = {"emotions": { "anger" : 1, "disgust" : 0, "fear" : 0, "joy" : 0, "sadness" : 0}, "strongest" : 'anger', "color" : "#FFFFFF" }
temp_emotions = { "anger" : 1, "disgust" : 0, "fear" : 0, "joy" : 0, "sadness" : 0}
print "Test 1: Angry City"
print "~Preset Values (emotional average for a given city)"
print "     Anger: {}".format(temp_emotions["anger"])
print "     Disgust: {}".format(temp_emotions["disgust"])
print "     Fear: {}".format(temp_emotions["fear"])
print "     Joy: {}".format(temp_emotions["joy"])
print "     Sadness: {}".format(temp_emotions["sadness"])
CityEmotionAnalyzer.determine_hex_color(city)
print "~Expected Strongest Emotion: anger"
print "~Expected Hex Color: #f00"
print "->Output Strongest City: {}".format(city["strongest"])
print "->Output Hex Color: {}".format(city["color"])
print ""
# Test2
city = {"emotions": { "anger" : 0, "disgust" : 0, "fear" : 1, "joy" : 0, "sadness" : 0}, "strongest" : 'anger', "color" : "#FFFFFF" }
temp_emotions = { "anger" : 0, "disgust" : 0, "fear" : 1, "joy" : 0, "sadness" : 0}
print "Test 2: Fearful City"
print "~Preset Values (emotional average for a given city)"
print "     Anger: {}".format(temp_emotions["anger"])
print "     Disgust: {}".format(temp_emotions["disgust"])
print "     Fear: {}".format(temp_emotions["fear"])
print "     Joy: {}".format(temp_emotions["joy"])
print "     Sadness: {}".format(temp_emotions["sadness"])
CityEmotionAnalyzer.determine_hex_color(city)
print "~Expected Strongest Emotion: fear"
print "~Expected Hex Color: #c0f"
print "->Output Strongest Emotion: {}".format(city["strongest"])
print "->Output Hex Color: {}".format(city["color"])
print ""
#Test3
city = {"emotions": { "anger" : 0, "disgust" : 0, "fear" : 0, "joy" : 0, "sadness" : 1}, "strongest" : 'anger', "color" : "#FFFFFF" }
temp_emotions = { "anger" : 0, "disgust" : 0, "fear" : 0, "joy" : 0, "sadness" : 1}
print "Test 3: Sad City"
print "~Preset Values (emotional average for a given city)"
print "     Anger: {}".format(temp_emotions["anger"])
print "     Disgust: {}".format(temp_emotions["disgust"])
print "     Fear: {}".format(temp_emotions["fear"])
print "     Joy: {}".format(temp_emotions["joy"])
print "     Sadness: {}".format(temp_emotions["sadness"])
CityEmotionAnalyzer.determine_hex_color(city)
print "~Expected Strongest Emotion: sadness"
print "~Expected Hex Color: #00f"
print "->Output Strongest City: {}".format(city["strongest"])
print "->Output Hex Color: {}".format(city["color"])
