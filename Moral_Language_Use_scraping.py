# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 21:55:24 2023

@author: Alex
"""

# Imports

import snscrape.modules.twitter as sntwitter
import pandas as pd
import os
import datetime
import numpy as np
import seaborn as sns
from nltk.corpus import wordnet as wn
import itertools
import nltk
import contractions
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import ast
from glob import glob
import collections
from scipy import stats

# setwd

os.chdir("C:/Users/Alex/Desktop/Uni/Master Psychologie/WS 22/SE CSS/Final Project/project/congress twitter handles")


# make lists of senators; note on periods:
    ## 114: since:2015-01-01 until:2016-12-31
    ## 115: since:2017-01-01 until:2018-12-31
    ## 116: since:2019-01-01 until:2020-12-31
    ## 117: since:2021-01-01 until:2022-12-31

df_114 = pd.read_excel("114th congress list.xlsx")
df_115 = pd.read_excel("115th congress list.xlsx")
df_116 = pd.read_excel("116th congress list.xlsx")
df_117 = pd.read_excel("117th congress list.xlsx")

senators_114 = list(df_114["Handle"])
senators_115 = list(df_115["Handle"])
senators_116 = list(df_116["Handle"])
senators_117 = list(df_117["Handle"])


# Scraping

## Limit maxTweets

maxTweets = 1500

## 114 congress

### Creating list to append tweet data to

tweets_list114 = []

### scrape that shit

for sen in senators_114:

### Using TwitterSearchScraper to scrape data 
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper(f'from:{sen} since:2015-01-01 until:2016-12-31').get_items()):
        if i>=maxTweets:
            break
        tweets_list114.append([tweet.date, tweet.id, tweet.content, tweet.user.username])

### Creating a dataframe from the tweets list above 
tweets_114 = pd.DataFrame(tweets_list114, columns=['Datetime', 'Tweet Id', 'Text', 'Username'])

### convert Datetime and make year variable

tweets_114["Datetime"] = pd.to_datetime(tweets_114["Datetime"])
tweets_114["Year"] = tweets_114["Datetime"].dt.year


## 115 congress

# Creating list to append tweet data to

tweets_list115 = []

# scrape that shit

for sen in senators_115:

# Using TwitterSearchScraper to scrape data 
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper(f'from:{sen} since:2017-01-01 until:2018-12-31').get_items()):
        if i>=maxTweets:
            break
        tweets_list115.append([tweet.date, tweet.id, tweet.content, tweet.user.username])

# Creating a dataframe from the tweets list above 
tweets_115 = pd.DataFrame(tweets_list115, columns=['Datetime', 'Tweet Id', 'Text', 'Username'])

# convert Datetime and make year variable

tweets_115["Datetime"] = pd.to_datetime(tweets_115["Datetime"])
tweets_115["Year"] = tweets_115["Datetime"].dt.year


## 116 congress

# Creating list to append tweet data to

tweets_list116 = []

# scrape that shit

for sen in senators_116:

# Using TwitterSearchScraper to scrape data 
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper(f'from:{sen} since:2019-01-01 until:2020-12-31').get_items()):
        if i>=maxTweets:
            break
        tweets_list116.append([tweet.date, tweet.id, tweet.content, tweet.user.username])

# Creating a dataframe from the tweets list above 
tweets_116 = pd.DataFrame(tweets_list116, columns=['Datetime', 'Tweet Id', 'Text', 'Username'])

# convert Datetime and make year variable

tweets_116["Datetime"] = pd.to_datetime(tweets_116["Datetime"])
tweets_116["Year"] = tweets_116["Datetime"].dt.year


## 117 congress

# Creating list to append tweet data to

tweets_list117 = []

# scrape that shit

for sen in senators_117:

# Using TwitterSearchScraper to scrape data 
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper(f'from:{sen} since:2021-01-01 until:2022-12-31').get_items()):
        if i>=maxTweets:
            break
        tweets_list117.append([tweet.date, tweet.id, tweet.content, tweet.user.username])

# Creating a dataframe from the tweets list above 
tweets_117 = pd.DataFrame(tweets_list117, columns=['Datetime', 'Tweet Id', 'Text', 'Username'])

# convert Datetime and make year variable

tweets_117["Datetime"] = pd.to_datetime(tweets_117["Datetime"])
tweets_117["Year"] = tweets_117["Datetime"].dt.year



# export to csv

os.chdir("C:/Users/Alex/Desktop/Uni/Master Psychologie/WS 22/SE CSS/Final Project/project/data")

tweets_114.to_csv("tweets_114_full.csv")
tweets_115.to_csv("tweets_115_full.csv")
tweets_116.to_csv("tweets_116_full.csv")
tweets_117.to_csv("tweets_117_full.csv")
