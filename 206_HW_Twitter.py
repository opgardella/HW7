import unittest
import tweepy
import requests
import json
import twitter_info		# you need to initialize this file with your Tweet app info
import urllib.request, urllib.parse, urllib.error

## SI 206 - HW
## COMMENT WITH:
## Name: Olivia Gardella
## Your section day/time: Thursday 3-4pm
## Any names of people you worked with on this assignment: Julie Burke, Hana Bezark


## Write code that uses the tweepy library to search for tweets with three different phrases of the
## user's choice (should use the Python input function), and prints out the Tweet text and the
## created_at value (note that this will be in GMT time) of the first FIVE tweets with at least
## 1 blank line in between each of them, e.g.


## You should cache all of the data from this exercise in a file, and submit the cache file
## along with your assignment.

## So, for example, if you submit your assignment files, and you have already searched for tweets
## about "rock climbing", when we run your code, the code should use CACHED data, and should not
## need to make any new request to the Twitter API.  But if, for instance, you have never
## searched for "bicycles" before you submitted your final files, then if we enter "bicycles"
## when we run your code, it _should_ make a request to the Twitter API.

## Because it is dependent on user input, there are no unit tests for this -- we will
## run your assignments in a batch to grade them!

## We've provided some starter code below, like what is in the class tweepy examples.

##SAMPLE OUTPUT
## See: https://docs.google.com/a/umich.edu/document/d/1o8CWsdO2aRT7iUz9okiCHCVgU5x_FyZkabu2l9qwkf8/edit?usp=sharing

#to take care of Unicode error
import sys
def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
    enc = file.encoding
    if enc == 'UTF-8':
        print(*objects, sep=sep, end=end, file=file)
    else:
        f = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
        print(*map(f, objects), sep=sep, end=end, file=file)

## **** For extra credit, create another file called twitter_info.py that
## contains your consumer_key, consumer_secret, access_token, and access_token_secret,
## import that file here.  Do NOT add and commit that file to a public GitHub repository.

## **** If you choose not to do that, we strongly advise using authentication information
## for an 'extra' Twitter account you make just for this class, and not your personal
## account, because it's not ideal to share your authentication information for a real
## account that you use frequently.

## Get your secret values to authenticate to Twitter. You may replace each of these
## with variables rather than filling in the empty strings if you choose to do the secure way
## for EC points
consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret

## Set up your authentication to Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
# Set up library to grab stuff from twitter with your authentication, and
# return it in a JSON-formatted way

api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

## Write the rest of your code here!

#### Recommended order of tasks: ####
## 1. Set up the caching pattern start -- the dictionary and the try/except
## 		statement shown in class.

#initiate the cache file
CACHE_FNAME = 'twitter_results.json' # String for your file. We want the JSON file type, bcause that way, we can easily get the information into a Python dictionary!

#try to open the cache and read it
try:
    cache_file = open(CACHE_FNAME, 'r') # Try to read the data from the file
    cache_contents = cache_file.read()  # If it's there, get it into a string
    CACHE_DICTION = json.loads(cache_contents) # And then load it into a dictionary
    cache_file.close() # Close the file, we're good, we got the data in a dictionary.
#or else make an empty dictionary
except:
    CACHE_DICTION = {}



## 2. Write a function to get twitter data that works with the caching pattern,
## 		so it either gets new data or caches data, depending upon what the input
##		to search for is.


def get_twitter(search_term):
    #if the term is already in the cache, just get it from there
    if search_term in CACHE_DICTION:
        print("using cache")
        return CACHE_DICTION[search_term]
    #if it is not already in the cache, use twitter results
    else:
        print("fetching")
        results = api.search(search_term)
        #try to add it to the cache
        try:
            CACHE_DICTION[search_term] =  json.dumps(results)
            dumped_json_cache = json.dumps(CACHE_DICTION)
            fw = open(CACHE_FNAME,"w")
            fw.write(dumped_json_cache)
            fw.close() # Close the open file
            return CACHE_DICTION[search_term]
        #if there is something wrong, print that it wasn't a valid search
        except:
            print("Wasn't in cache and wasn't valid search either")
            return None



## 3. Using a loop, invoke your function, save the return value in a variable, and explore the
##		data you got back!

#have c be a counter
c = 0
#have the while loop run 3 times
while c < 3:
    #have users input the tweet term they want to search
    tweet_term = input('Enter Tweet term: ')
    #if user just presses enter, break
    if len(tweet_term) < 1: break
    #get data from get_twitter function
    data = get_twitter(tweet_term) #data is a dict
    #increment c
    c += 1
    data_dict = json.loads(data)
    #print (data)
    #print(type(data))
    #print(type(data_dict))


## 4. With what you learn from the data -- e.g. how exactly to find the
##		text of each tweet in the big nested structure -- write code to print out
## 		content from 5 tweets, as shown in the linked example.

    for tweet in data_dict['statuses'][0:5]:
        #find the text and time created for each tweet the user searches
        text = tweet['text']
        created_at = tweet['created_at']
        #return the text and created at
        uprint ('TEXT:', text)
        uprint ('CREATED AT:', created_at)
        print ('\n')
