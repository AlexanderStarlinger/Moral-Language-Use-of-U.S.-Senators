# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 23:34:23 2023

@author: Alex
"""

# setup

## imports

import snscrape.modules.twitter as sntwitter
import pandas as pd
import os
import datetime
import numpy as np
import seaborn as sns
import regex as re
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
import preprocessor as p

lemma = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))

## preprocessing pipeline 

def clean_url(input):
    output = re.sub(r"http\S+", "", input)
    return output


def fix_contraction(input):
    output = contractions.fix(input)
    return output


def clean_non_alphanumeric(input):
    output = re.sub(r"[^a-zA-Z0-9]", " ", input)
    return output


def clean_tokenization(input):
    output = nltk.word_tokenize(input)
    return output


def clean_stopwords(input):
    output = [item for item in input if item not in stop_words]
    return output


def clean_lowercase(input):
    output = str(input).lower()
    return output


def clean_lemmatization(input):
    output = [lemma.lemmatize(word=w, pos="v") for w in input]
    return output


def clean_length(input):
    output = [word for word in input if len(word) > 2]
    return output


def convert_to_string(input):
    output = " ".join(input)
    return output


def preprocessing(text, remove_stopwords=True):
    """
    Preprocessing pipeline.
    """
    text = clean_url(text)
    text = fix_contraction(text)
    text = clean_non_alphanumeric(text)
    text = clean_lowercase(text)
    text = clean_tokenization(text)
    if remove_stopwords:
        text = clean_stopwords(text)
    text = clean_lemmatization(text)
    text = clean_length(text)
    text = convert_to_string(text)
    return text


## function for 


# import df

## setwd

os.chdir("C:/Users/Alex/Desktop/Uni/Master Psychologie/WS 22/SE CSS/Final Project/project/data")

tweets_df = pd.read_csv("tweets_df_full.csv")


# clean

## 1) tweet-preprocessor


tweets_df["Text_processed"] = tweets_df["Text"].apply(p.clean)


## 2) own pipeline (classes)

tweets_df["Text_processed"] = tweets_df["Text_processed"].apply(preprocessing)

tweets_df["Text_processed"] = tweets_df["Text_processed"].apply(lambda txt: str(txt.split(" ")))

## delete text

tweets_df = tweets_df.drop(["Text", "Unnamed: 0"], axis = 1)

# export to csv

os.chdir("C:/Users/Alex/Desktop/Uni/Master Psychologie/WS 22/SE CSS/Final Project/project/data")

tweets_df.to_csv("tweets_preprocessed_full.csv")



