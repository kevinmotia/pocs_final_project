

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
import time
#from fuzzywuzzy import fuzz    No longer used. Geotext replaces this. 
from geotext import GeoText
#-------------------------------------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------------------------------------
# Store bearer_token in variable
bearer_token = "AAAAAAAAAAAAAAAAAAAAAHIxjgEAAAAAHBtpIV5008WAMdj3Hd2dapo%2BM6k%3DGfV9iH7qSwlBf8UQcODVI6DW0FaoIT6tfodr38XcVR018cGh6v"
client = tweepy.Client(bearer_token=bearer_token, wait_on_rate_limit=True)
# Replace with your own search query
query = ' ("send them back to" OR "send him back to" OR "send her back to" OR "illegals from" OR "illegal aliens from" OR "illegal alien from" OR "illegal immigrants from" OR "illegal immigrant from" OR "illegal criminals from" OR "illegal criminal from" OR "foreign criminals from" OR "foreign criminal from" OR "illegal terrorist from" OR "sending us their criminals" OR "ban people from" OR "deport them" OR "deport people from" OR "deport all these" OR "immigrants from" OR "invading our country" OR "being invaded" OR "invaders" OR "immigrants") place_country:US -is:retweet' 
# Replace with time period of your choice
start_time = '2012-03-05T00:00:00Z' 
# Replace with time period of your choice
end_time = '2022-12-05T00:00:00Z'
tweets = tweepy.Paginator(client.search_all_tweets, query=query,
                              tweet_fields=['created_at'], start_time = start_time, end_time = end_time, max_results=100).flatten(limit=550000)
#-------------------------------------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------------------------------------
# Append tweet information to lists
sentiment_list = []
id_list = []
created_at_list = []
tweet_list = []
for tweet in tweets:
    sentiment_list.append('0')
    id_list.append(tweet.id)
    created_at_list.append(tweet.created_at)
    tweet_list.append(tweet.text)
    time.sleep(.02) # changed from 1 to .5, .15 seemed to work too. .04 seems to work too. .03 seems to work.

# Save original tweets
tweet_dic_original = {'sentiment':sentiment_list, 'id':id_list, 'date':created_at_list, 'text':tweet_list} # changed to text_list from clean_tweet_list
df_tweets_original = pd.DataFrame(tweet_dic_original, columns = ['sentiment','id','date','text'])
df_tweets_original.to_csv('originalTweets.csv', index = False)

cleaned_tweet_list = []
for tweet in tweet_list:                                              # for each tweet  
    tweet = tweet.lower()                                             # make it all lowercase
    temp = re.sub(r'http\S+', '', tweet)                              # take out URLs
    temp = re.sub(r'(@\S+) | (#\S+)', r'', temp)                      # take out @s and hashtags
    temp = re.sub(r'https.*|(?![0-9À-ÿa-z\s]).','', temp)            # take out URLs
    temp = re.sub(r'\s{2,}', ' ', temp)                               # clean up extra spaces
    cleaned_tweet_list.append(temp)                                  


tweet_dic = {'sentiment':sentiment_list, 'id':id_list, 'date':created_at_list, 'text':cleaned_tweet_list} # changed to text_list from clean_tweet_list
df_tweets = pd.DataFrame(tweet_dic, columns = ['sentiment','id','date','text'])




# tweets_with_mentions = []
# for tweet in cleaned_tweet_list:
#     places = GeoText(tweet, aggressive = True).country_mentions         # get the regions mentioned
    
##     region_list = list(places.keys())    #needs double comments because it has the word region in it so pylance is being weird
#  #   print(region_list)
#     for entry in region_list:
#         if 'Europe' in entry:
#             tweets_with_mentions.append(tweet)
#         if 'Latin America' in entry:
#             tweets_with_mentions.append(tweet)
#         if 'North America' in entry:
#             tweets_with_mentions.append(tweet)
#         if 'Indian Subcontinent' in entry:
#             tweets_with_mentions.append(tweet)
#         if 'Sub-Saharan Africa' in entry:
#             tweets_with_mentions.append(tweet)
#         if 'MENA' in entry:
#             tweets_with_mentions.append(tweet)
#         if 'East Asia' in entry:
#             tweets_with_mentions.append(tweet)
#         if 'Central Asia' in entry:
#             tweets_with_mentions.append(tweet)
#         if 'Pacific' in entry:
#             tweets_with_mentions.append(tweet)
# #print(tweets_with_mentions)

df_tweetsWithNames = pd.DataFrame(columns=['sentiment', 'id', 'date', 'text'])                  # initialize df_tweetsWithNames 



for tweetIndex in range(len(df_tweets)):
    places = GeoText(df_tweets['text'][tweetIndex], aggressive = True).country_mentions         # get the regions mentioned

    region_list = list(places.keys())
    #   print(region_list)
    for entry in region_list:
        if 'Europe' in entry:
            df_tweetsWithNames = df_tweetsWithNames.append(df_tweets.iloc[[tweetIndex]])         # Add tweetinfo of tweets with Europe mentions
        if 'Latin America' in entry:
            df_tweetsWithNames = df_tweetsWithNames.append(df_tweets.iloc[[tweetIndex]])         # Add tweetinfo of tweets with Latin America mentions
        if 'North America' in entry:
            df_tweetsWithNames = df_tweetsWithNames.append(df_tweets.iloc[[tweetIndex]])         # Add tweetinfo of tweets with North America mentions
        if 'Indian Subcontinent' in entry:
            df_tweetsWithNames = df_tweetsWithNames.append(df_tweets.iloc[[tweetIndex]])         # Add tweetinfo of tweets with Indian Subcontinent mentions
        if 'Sub-Saharan Africa' in entry:
            df_tweetsWithNames = df_tweetsWithNames.append(df_tweets.iloc[[tweetIndex]])         # Add tweetinfo of tweets with Sub-Saharan Africa mentions
        if 'MENA' in entry:
            df_tweetsWithNames = df_tweetsWithNames.append(df_tweets.iloc[[tweetIndex]])         # Add tweetinfo of tweets with MENA mentions
        if 'East Asia' in entry:
            df_tweetsWithNames = df_tweetsWithNames.append(df_tweets.iloc[[tweetIndex]])         # Add tweetinfo of tweets with East Asia mentions
        if 'Central Asia' in entry:
            df_tweetsWithNames = df_tweetsWithNames.append(df_tweets.iloc[[tweetIndex]])         # Add tweetinfo of tweets with Europe mentions
        if 'Pacific' in entry:
            df_tweetsWithNames = df_tweetsWithNames.append(df_tweets.iloc[[tweetIndex]])         # Add tweetinfo of tweets with Pacific mentions

#df_tweetsWithNames = df_tweetsWithNames.reset_index()                                            # Reset df_tweetsWithNames index
df_tweetsWithNames = df_tweetsWithNames.drop_duplicates()                                        # Drop duplicate entries
df_tweetsWithNames = df_tweetsWithNames.sort_values('id')                                        # sort tweets from newest to oldest by using the id.... Larger value means newer

df_tweetsWithNames.to_csv('dec11Tweets.csv', index = False)                          # Writing df_tweetsWithNames to a csv














# # initialize dataframe filtered for tweets with country or region names mentioned
# df_tweetsWithNames = pd.DataFrame(columns=['sentiment', 'id', 'date', 'text'])

# for tweetIndex in range(len(df_tweets)):
#     word_tokens = word_tokenize(df_tweets['text'][tweetIndex])      # tokenize tweet
#     for token in word_tokens:               # for each token
#         for name in globe_df['Country']:
#             fuzzRatio = fuzz.token_set_ratio(token, name)
#             if fuzzRatio >= .90:
#                 df_tweetsWithNames = df_tweetsWithNames.append(df_tweets.iloc[[tweetIndex]])      



# Sort Tweets by newest to oldest      (Oldest 1000 tweets as a train/test dataset. The rest will be our unevaluated data)
# df_tweetsWithNames.sort_values('id')


# # Convert df_tweetsWithNames to csv file
# df_tweetsWithNames.to_csv('trainingTweetsWithNames.csv', index = False)











#-------------------------------------------------------------------------------------------------------------------------------
# Put lists in a dictionary
# tweet_dic = {'sentiment':sentiment_list, 'id':id_list, 'date':created_at_list, 'text':tweetsWithNames} # changed to text_list from clean_tweet_list
# # Convert dictionary to dataframe
# df = pd.DataFrame(tweet_dic, columns = ['sentiment','id','date','text'])

# print(df)
# df.sort_values('id')                                                       # Sorting by id will also sort from newest to oldest
# print('--------------------HelloThere!---------------------')
# print(df)
# df.to_csv('trainingTweetsHELLO.csv', index = False)  

#-------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------
# I have edited this file to not remove stopwords. You can replace the lines with the commented our ones to remove them once again if that's necessary.