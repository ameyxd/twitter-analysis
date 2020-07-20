import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
# import timeline
import os
import matplotlib
matplotlib.use('Qt5Agg')

tweets = []
with open(os.getcwd() + '/data/timeline.json', 'r') as f:
    data = json.load(f)

for tweet in data:
    retweet = 'RT @' in tweet['text']
    pic = False
    if 'media' in tweet['entities']:
        pic = True
    geo, coord = tweet['geo'], tweet['coordinates']
    retweet_cnt, fav_cnt = tweet['retweet_count'], tweet['favorite_count']
    date = datetime.datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S %z %Y')

    tweets.append([tweet['text'], retweet, pic, date, retweet_cnt, fav_cnt])

df = pd.DataFrame(tweets, columns=['Tweet', 'is_RT', 'is_pic', 'Date', 'RT_cnt', 'fav_cnt'])
df.index = pd.to_datetime(df['Date'])
df = df.drop(columns=['Date'])

my_tweets = df[~df['is_RT']]
my_tweets = my_tweets.sort_index()

retweets = df[df['is_RT']]
retweets = retweets.sort_index()

total_retweets = retweets.resample('M').count()
total_tweets = df.resample('M').count()

summary = pd.DataFrame(columns=['Tweets', 'Retweets', 'RTPerc'])
summary.Tweets = total_tweets.Tweet
summary.Retweets = total_retweets.Tweet
summary.RTPerc =summary.Retweets/summary.Tweets
summary.fillna(0)

# summary.Tweets.plot()
# summary.Retweets.plot()
summary.plot(subplots=True)
plt.show()

# # TODO:
#     1. WordCloud of tweets
#     2. Tweets with pictures
#     3. Most liked and favorited
#     4. Increase in engagement
#     5. Rise in followers
