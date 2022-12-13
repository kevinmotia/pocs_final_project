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


tweet_list = ['hey @president, what are you doing? #dontknow', 'here is a url http://www.idk.com', 'heres another www.hello.com', 'hey!!!!']

cleaned_tweet_list = []
for tweet in tweet_list:                                              # for each tweet  
    tweet = tweet.lower()                                             # make it all lowercase
    temp = re.sub(r'http\S+', r'', tweet)                              # take out URLs
    temp = re.sub(r'www.\S+', r'', tweet)                              # take out URLs

    temp = re.sub(r'(@\S+) | (#\S+)', r'', temp)                      # take out @s and hashtags
    temp = re.sub(r'https.*|(?![0-9À-ÿa-z\s]).',r'', temp)            # take out URLs
    temp = re.sub(r'\s{2,}', ' ', temp)                               # clean up extra spaces

    cleaned_tweet_list.append(temp)         


print(cleaned_tweet_list)