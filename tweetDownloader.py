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
from geotext import GeoText

def Download_Tweets(bearer_token, query, start_time, end_time):
  client = tweepy.Client(bearer_token=bearer_token, wait_on_rate_limit=True)
  query = ' ("send them back to" OR "send him back to" OR "send her back to" OR "illegals from" OR "illegal aliens from" OR "illegal alien from" OR "illegal immigrants from" OR "illegal immigrant from" OR "illegal criminals from" OR "illegal criminal from" OR "foreign criminals from" OR "foreign criminal from" OR "illegal terrorist from" OR "sending us their criminals" OR "ban people from" OR "deport them" OR "deport people from" OR "deport all these" OR "immigrants from" OR "invading our country" OR "being invaded" OR "invaders" OR "immigrants") place_country:US -is:retweet' 
  tweets = tweepy.Paginator(client.search_all_tweets, query=query,
                                tweet_fields=['created_at'], start_time = start_time, end_time = end_time, max_results=100).flatten(limit=550000)

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
      time.sleep(.02) # used to deal with rate limit

  # Save original tweets
  tweet_dic_original = {'sentiment':sentiment_list, 'id':id_list, 'date':created_at_list, 'text':tweet_list} # changed to text_list from clean_tweet_list
  df_tweets_original = pd.DataFrame(tweet_dic_original, columns = ['sentiment','id','date','text'])
  df_tweets_original.to_csv('originalTweets.csv', index = False)
 
