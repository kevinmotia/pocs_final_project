
import tweetDownloader as TWEET_DOWNLOADER
import tweetSorter as TWEET_SORTER

bearer_token =  "AAAAAAAAAAAAAAAAAAAAAHIxjgEAAAAAHBtpIV5008WAMdj3Hd2dapo%2BM6k%3DGfV9iH7qSwlBf8UQcODVI6DW0FaoIT6tfodr38XcVR018cGh6v" # can leave public, no longer used.
query = ' ("send them back to" OR "send him back to" OR "send her back to" OR "illegals from" OR "illegal aliens from" OR "illegal alien from" OR "illegal immigrants from" OR "illegal immigrant from" OR "illegal criminals from" OR "illegal criminal from" OR "foreign criminals from" OR "foreign criminal from" OR "illegal terrorist from" OR "sending us their criminals" OR "ban people from" OR "deport them" OR "deport people from" OR "deport all these" OR "immigrants from" OR "invading our country" OR "being invaded" OR "invaders" OR "immigrants") place_country:US -is:retweet' 
# Replace with time period of your choice
start_time = '2012-03-05T00:00:00Z' 
# Replace with time period of your choice
end_time = '2022-12-05T00:00:00Z'

# download tweets and write them to a CSV file
TWEET_DOWNLOADER.Download_Tweets(bearer_token, query, start_time, end_time)
# open the CSV file, clean the tweets, and sort them by region they mention. Write sorted tweets to a CSV file
TWEET_SORTER.Get_Tweets_With_Mentions('originalTweets.csv')
