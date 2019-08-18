#!/usr/bin/python3

import tweepy
import config
import rowData

# Authenticate to Twitter
auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_token_secret)

# Create API object
api = tweepy.API(auth)


# Tweet Msg Format 

def setupTweet(data: rowData):
    msgFormat = data.title + "\n\n" + "Type: " + data.category + "\n" + "Sale Price: " + data.price + "\n" + data.url
    postTweet(msgFormat)
    
# Create a Tweet
def postTweet(msg):
    api.update_status(msg)
    
    
    
    
if __name__ == "__main__":
    print("Twitter Bot Running")