import twitter
import os
import json
from auth_keys import ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET

api = twitter.Api(consumer_key=CONSUMER_KEY,
                  consumer_secret=CONSUMER_SECRET,
                  access_token_key=ACCESS_TOKEN_KEY,
                  access_token_secret=ACCESS_TOKEN_SECRET)

friends = api.GetFriends()
print([f.name for f in friends])

followers = api.GetFollowers()
print([f.name for f in followers])

favs = api.GetFavorites(count=200)
print(len(favs))

for fav in favs:
    print(fav.text)

retweets = api.GetUserRetweets(count=10000)
print(len(retweets))

tweets = api.GetUserTimeline(count=10000)
print(len(tweets))


def get_tweets(api=None, screen_name=None):
    timeline = api.GetUserTimeline(screen_name=screen_name, count=200)
    earliest_tweet = min(timeline, key=lambda x: x.id).id
    print("getting tweets before:", earliest_tweet)

    while True:
        tweets = api.GetUserTimeline(
            screen_name=screen_name, max_id=earliest_tweet, count=200
        )
        new_earliest = min(tweets, key=lambda x: x.id).id

        if not tweets or new_earliest == earliest_tweet:
            break
        else:
            earliest_tweet = new_earliest
            print("getting tweets before:", earliest_tweet)
            timeline += tweets

    return timeline


timeline = get_tweets(api=api)
print(len(timeline))

with open(os.getcwd() + '/data/timeline.json', 'w+') as f:
    a = []
    for tweet in timeline:
        a.append(tweet._json)
    f.write(json.dumps(a))

