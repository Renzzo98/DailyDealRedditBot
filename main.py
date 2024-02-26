#!/usr/bin/python

#import tweet
import praw 
import rowData
import csvFactory
import random
import configparser


keywordFlag = False

# Create a ConfigParser instance
config = configparser.ConfigParser()

# Read the INI file
config.read('praw.ini')

reddit = praw.Reddit(
    client_id = config['RedditAcccount']['clientID'],
    client_secret = config['RedditAcccount']['clientSecret'],
    user_agent = config['RedditAcccount']['userAgent']
)
subreddit = reddit.subreddit('buildapcsales')

def parsingRisingDeals():
    Posted = False
    for submission in subreddit.rising(limit=5):
        title = submission.title
        print("Title: ", title)
        part = identifyPCPart(title)
        print("Part: ", part)
        price = getPrice(title)
        print("Price: ", price)
        #print("Score: ", submission.score)
        url = submission.url
        print("URL: ", url)
        print("--------------------------------\n")
        data = rowData.RowData(title,part,price,url)
        Posted = preparingTweet(data)
        if (Posted):
            break
    print ("Tweet Posted")
    
def parsingHotDeals():
    Posted = False
    for submission in subreddit.hot(limit=5):
        title = submission.title
        print("Title: ", title)
        part = identifyPCPart(title)
        print("Part: ", part)
        price = getPrice(title)
        print("Price: ", price)
        #print("Score: ", submission.score)
        url = submission.url
        print("URL: ", url)
        print("--------------------------------\n")
        data = rowData.RowData(title,part,price,url)
        Posted = preparingTweet(data)
        if (Posted):
            break
    print ("Tweet Posted")

def parsingNewDeals():
    Posted = False
    for submission in subreddit.new(limit=5):
        title = submission.title
        print("Title: ", title)
        part = identifyPCPart(title);
        print("Part: ", part)
        price = getPrice(title)
        print("Price: ", price)
        #print("Score: ", submission.score)
        url = submission.url
        print("URL: ", url)
        print("--------------------------------\n")
        data = rowData.RowData(title,part,price,url)
        Posted = preparingTweet(data)
        if (Posted):
            break
    print ("Tweet Posted")


def preparingTweet(data):
    result = csvFactory.checkPrevPosted(data.title)
    if (result):
        csvFactory.appendToDatabase(data)
        # tweet.setupTweet(data)
        return True
    else:
        return False

# Works for buildPC only
def identifyPCPart(title):
    if (title != None):
        partID = ""
        recording = False
        for char in title:
            if (char == "["):
                recording = True
            elif (char == "]"):
                recording = False
            else:
                if (recording):
                    partID += char
        return partID.upper()
    else:
        raise ValueError("Title was not provided when identifing Part")

def getPrice(title):
    if (title != None):
        price = ""
        recording = False
        firstPriceInx = 0
        for char in title:
            if (char == "$"):
                recording = True
                firstPriceInx += 1
            elif (char == "(" or char == ")"):
                recording = False
            else:
                if (recording and firstPriceInx == 1):
                    price += char
        return price
    else:
        raise ValueError("Title was not provided when getting the price")
    

def keywordChecker():
    keywords = input("What keywords do you want to search with? Separate them by commas\n")
    keywordsArr = [x.strip() for x in keywords.split(',')]
    index = 0
    while index < len(keywordsArr):
        keywordsArr[index] = keywordsArr[index].upper()
        index += 1

    print ("TEST: ", keywordsArr)

def DecisionTree():
    keywordDec = input("Are you looking for a specific part? Y or N?\n")
    keywordDec = keywordDec.upper()
    if (keywordDec == "YES" or keywordDec == "Y"):
        global keywordFlag 
        keywordFlag = True
        keywordChecker()
        randomSearch()
    else:
        randomSearch()

def randomSearch():
    randInt = random.randint(1,11)
    decidingSearchType(randInt)
    
def decidingSearchType(randInt: int):
    if (randInt != None):
        if (randInt >= 1 and randInt < 4):
            print("Search Rising")
            parsingRisingDeals()
        if (randInt >= 4 and randInt < 7):
            print("Search Hot")
            parsingHotDeals()
        else:
            print("Search New")
            parsingNewDeals()
        
if __name__ == "__main__":
    randomSearch()