# Imports
import tweepy
import json
import csv
from itertools import chain
import pandas as pd
import numpy as np
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
from geotext import GeoText

# Read in files to dataFrames
tweets_df = pd.read_csv('originalTweets.csv')#, dtype={'sentiment':str, 'id':str, 'date':str, 'text':str})

print(type('sentiment'))
print(type('id'))
print(type('date'))
print(type('text'))


sentiment_list=[]
for entry in tweets_df['sentiment']:
    sentiment_list.append(str(entry))

id_list=[]
for entry in tweets_df['id']:
    id_list.append(str(entry))

date_list=[]
for entry in tweets_df['date']:
    date_list.append(str(entry))


initial_tweets=[]
for entry in tweets_df['text']:
    initial_tweets.append(str(entry))



print(type(initial_tweets[0]))
print(initial_tweets[0:20])


cleaned_tweet_list = []
for tweet in initial_tweets:                                              # for each tweet  
    tweet = tweet.lower()                                             # make it all lowercase
    temp = re.sub(r'http\S+', r'', tweet)                              # take out URLs
    temp = re.sub(r'www.\S+', r'', temp)                              # take out URLs

    temp = re.sub(r'(@\S+) | (#\S+)', r'', temp)                      # take out @s and hashtags
    temp = re.sub(r'https.*|(?![0-9À-ÿa-z\s]).',r' ', temp)            # take out URLs  # Replace them with a space. This will be removed when extra spaces are removed
    temp = re.sub(r'\s{2,}', ' ', temp)                               # clean up extra spaces

    cleaned_tweet_list.append(temp)     

print('--------------------')
print(cleaned_tweet_list[0:20])  

tweets_df['text'] = cleaned_tweet_list



details = {'sentiment' : sentiment_list, 'id' : id_list, 'date' : date_list, 'text' : cleaned_tweet_list}
df_cleaned = pd.DataFrame(details, columns = ['sentiment', 'id', 'date', 'text'])

df_tweetsWithNames = pd.DataFrame(columns = ['sentiment', 'id', 'date', 'text'])



for tweetIndex in range(len(df_cleaned)):
    places = GeoText(df_cleaned['text'][tweetIndex], aggressive = True).country_mentions         # get the regions mentioned

    region_list = list(places.keys())
    #   print(region_list)
    for entry in region_list:
        if 'Europe' in entry:
            df_tweetsWithNames = df_tweetsWithNames.append(df_cleaned.iloc[[tweetIndex]])         # Add tweetinfo of tweets with Europe mentions
        if 'Latin America' in entry:
            df_tweetsWithNames = df_tweetsWithNames.append(df_cleaned.iloc[[tweetIndex]])         # Add tweetinfo of tweets with Latin America mentions
        if 'North America' in entry:
            df_tweetsWithNames = df_tweetsWithNames.append(df_cleaned.iloc[[tweetIndex]])         # Add tweetinfo of tweets with North America mentions
        if 'Indian Subcontinent' in entry:
            df_tweetsWithNames = df_tweetsWithNames.append(df_cleaned.iloc[[tweetIndex]])         # Add tweetinfo of tweets with Indian Subcontinent mentions
        if 'Sub-Saharan Africa' in entry:
            df_tweetsWithNames = df_tweetsWithNames.append(df_cleaned.iloc[[tweetIndex]])         # Add tweetinfo of tweets with Sub-Saharan Africa mentions
        if 'MENA' in entry:
            df_tweetsWithNames = df_tweetsWithNames.append(df_cleaned.iloc[[tweetIndex]])         # Add tweetinfo of tweets with MENA mentions
        if 'East Asia' in entry:
            df_tweetsWithNames = df_tweetsWithNames.append(df_cleaned.iloc[[tweetIndex]])         # Add tweetinfo of tweets with East Asia mentions
        if 'Central Asia' in entry:
            df_tweetsWithNames = df_tweetsWithNames.append(df_cleaned.iloc[[tweetIndex]])         # Add tweetinfo of tweets with Europe mentions
        if 'Pacific' in entry:
            df_tweetsWithNames = df_tweetsWithNames.append(df_cleaned.iloc[[tweetIndex]])         # Add tweetinfo of tweets with Pacific mentions

df_tweetsWithNames = df_tweetsWithNames.sample(frac=1)

df_tweetsWithNames.to_csv('cleanishTweetsRegion.csv', index = False)  