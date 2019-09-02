# Import the necessary package to process data in JSON format
try:
    import json
except ImportError:
    import simplejson as json

# Import the time, pandas, numpy, math, iso639, langid, matplotlib libraries
import time
import pandas as pd
import numpy as np
import math
import iso639 as iso
import langid as li
import matplotlib.pyplot as plt
from collections import OrderedDict

# Read the json in the file where tweets are collected
with open("collected_tweets2.txt", "r") as read_file:
    tweets = json.load(read_file)

# Create a dataframe from the tweets and saves them to a file,
df = pd.DataFrame.from_dict(tweets, orient = 'columns')
tweets_length = len(tweets)
print('Just give it some time...')
print(str(tweets_length) + ' total tweets collected.')
print('Just a few more minutes...')

# Remove all tweets that are retweets
texts = np.array(df['text'])
for i in range(0, tweets_length):
    try:
        first_two = str(texts[i])[:2]
    except:
        continue
    if 'RT' in first_two:
        texts = np.delete(texts, i)
        df.drop([i])

tweets_length = len(df['text'])

# Drops tweets that aren't geotagged
df2 = df.copy()
df2 = df2.dropna(subset=['place'])
locations = np.array(df2['place'])
print(df2)

# Counts locations of all tweets
loc_count  = {}
loc_length = len(locations)

for i in range(0, loc_length-1):
    current = str(locations[i])
    if current in loc_count.keys():
        loc_count[current] += 1
    else:
        loc_count[current] = 1

print(loc_count)

# Remove all non-USA tweets
loc_dict = {}
for item in locations:
   country = item['country']
   loc_dict[country] = item

# Create variables to handle langid tags
langs = np.array(df['lang'])
langs_count = {}
langs_length = len(langs)

# Counts each language of all tweets
for i in range(0, langs_length-1):
    current = str(langs[i])
    if current in langs_count.keys():
        langs_count[current] += 1
    else:
        langs_count[current] = 1

langs_found = len(langs_count)

# Removes undefined language tweets
langs_count = {key:val for key, val in  langs_count.items() if val != 'und'}

# Find out how many tweets were langid tagged
num_tagged = 0
for i in range(0, langs_length-1):
    if langs[i] != 'und':
        num_tagged += 1

percent_tagged = round(100*(num_tagged/langs_length), 2)

# Now, using langid API:
# Identifying all the languages by classifying the text of each tweet
texts2 = np.array(df['text'])
langs2 = []
langs2_count = {}

for current in df['text']:
    langs2.append(li.classify(current))

langs2_length = len(langs2)

# Counting occurrences of each language
for i in range(0, langs2_length-1):
    current = langs2[i][0]
    if current in langs2_count:
        langs2_count[current] += 1
    else:
        langs2_count[current] = 1

# Create dicts of the several most popular languages and countries
langs2_count = OrderedDict(sorted(langs2_count.items(), key=lambda kv: kv[1], reverse = True))
langs3_count = dict(list(langs2_count.items())[:10])

loc_count = OrderedDict(sorted(loc_count.items(), key=lambda kv: kv[1], reverse = True))
loc2_count = dict(list(loc_count.items())[:10])

# Plot the graphs
plt.bar(langs3_count.keys(), langs3_count.values(), color='g')
plt.title('Language usage from ' + str(tweets_length) + ' Tweets using Tweepy API')
plt.xlabel('Language ISO639 Code')
plt.ylabel('Number of tweets written in language')
plt.show()

plt.bar(loc2_count.keys(), loc2_count.values(), color='g')
plt.title('Geotags from ' + str(len(loc2_count)) + ' Tweets using Tweepy API')
plt.xlabel('Countries')
plt.ylabel('Number of tweets from country')
plt.show()

# Print question answers
# Question 2:
print()
print('Question 2:')
print('Of the ' + str(tweets_length) + ' tweets analyzed, about ' + str(percent_tagged) + '% of them were LangID tagged.')
print('Twitter provides 33 different language tags.')

for current, count in langs_count.items():
    current_percent = str(round(100*(count/langs_length), 2))
    try:
        print('Of the tweets language tagged, twitter says ' + current_percent + '% of them are ' + iso.to_name(current) + '.')
    except:
        print('Of the tweets language tagged, twitter says ' + current_percent + '% of them are ' + current + '.')

# Question 3:
print()
print('Question 3:')
for current, count in langs2_count.items():
    current_percent = str(round(100*(count/langs2_length), 2))
    try:
        print('Of the tweets language tagged, langid says ' + current_percent + '% of them are ' + iso.to_name(current) + '.')
    except:
        print('Of the tweets language tagged, langid says ' + current_percent + '% of them are ' + current + '.')

# Question 4
print()
print('Question 4: ')
percent_geo = str(round((loc_length/tweets_length)*100, 2))
print(percent_geo + '% of the collected tweets were geotagged.')
