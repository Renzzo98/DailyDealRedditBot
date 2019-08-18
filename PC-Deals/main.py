#!/usr/bin/python
import praw 
import tweet
import rowData
import csvFactory

keywordFlag = False

reddit = praw.Reddit('bot1')
subreddit = reddit.subreddit('buildapcsales')

def parsingDeals():
    Posted = False
    for submission in subreddit.rising(limit=5):
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
        tweet.setupTweet(data)
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
        parsingDeals()

        
    else:
        parsingDeals()

        
if __name__ == "__main__":
    DecisionTree()