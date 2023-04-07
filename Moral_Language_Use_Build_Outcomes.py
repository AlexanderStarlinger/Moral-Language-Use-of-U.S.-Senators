# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 15:21:32 2023

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


## function

def compute_frequencies(list_string, list_of_categories):
    """
    Function to calculate word frequencies.

    """

    global apply_counter1

    tokenized_text = ast.literal_eval(list_string)
    word_counter = collections.Counter(tokenized_text)
    total_words = len(tokenized_text)

    list_of_category_frequencies = []
    for category in list_of_categories:
        category_count = 0.0

        for word in category:
            category_count += int(word_counter[word])

        if total_words != 0 and category_count > 0:
            category_frequency = category_count / total_words
        else:
            category_frequency = float("nan")
        list_of_category_frequencies += [category_frequency]

    apply_counter1 += 1

    return list_of_category_frequencies

## import data (processed tweets)


os.chdir("C:/Users/Alex/Desktop/Uni/Master Psychologie/WS 22/SE CSS/Final Project/project/data")

tweets_processed = pd.read_csv("tweets_preprocessed_full.csv")



# BUILD OUTCOMES

## define dictionaries (list_of_categories)


harm_virtue = [r"safe.*", r"peace.*", r"compassion.*", r"empath.*", r"sympath.*", "care", r"protect.*", 
"shield", "shelter", "amity", r"secur.*", r"benefit.*", r"defen.*", r"guard.*", "preserve"]

harm_vice = [r"harm.*", r"suffer.*", "war",	"wars", r"warl.*", "warring",			r"fight.*",			r"violen.*",			r"hurt.*",		
"kill",			"kills",			r"killer.*",			"killed",			
"killing",			r"endanger.*",			r"cruel.*",			r"brutal.*",			r"abuse.*",			
r"damag.*",			r"ruin.*",		"ravage",			r"detriment.*",		r"crush.*",			r"attack.*",			
r"annihilate.*",		"destroy",			"stomp",			r"abandon.*",		"spurn",			"impair",			"exploit",		
"exploits",		"exploited",		"exploiting",		r"wound.*"]


fairness_virtue = ['fair',
'fairly',
'fairness',
r'fair.*',
r'fairmind.*',
'fairplay',
r'equal.*',
'justice',
'justness',
r'justifi.*',
r'reciproc.*',
r'impartial.*',
r'egalitar.*',
'rights',
'equity',
'equivalent',
'',
r'unbias.*',
'tolerant',
'equable',
r'balance.*',
'homologous',
r'unprejudice.*',
'reasonable',
'constant',
r'honest.*']


fairness_vice = [r'unfair.*',
r'unequal.*',
r'bias.*',
r'unjust.*',
r'injust.*',
r'bigot.*',
r'discriminat.*',
r'disproportion.*',
'inequitable',
r'prejud.*',
'dishonest',
'unscrupulous',
'dissociate',
'preference',
'favoritism',
r'segregat.*',
'exclusion',
r'exclud.*']

ingroup_virtue = ['together',
r'nation.*',
r'homeland.*',
'family',
'families',
'familial',
'group',
r'loyal.*',
'rpatriot.*',
'communal',
r'commune.*',
r'communit.*',
r'communis.*',
r'comrad.*',
'cadre',
r'collectiv.*',
'joint',
'unison',
r'unite.*',
r'fellow.*',
'guild',
'solidarity',
r'devot.*',
'member',
r'cliqu.*',
'cohort',
'ally',
'insider',
r'segregat.*']

ingroup_vice = [r'foreign.*',
r'enem.*',
r'betray.*',
r'treason.*',
r'traitor.*',
r'treacher.*',
r'disloyal.*',
r'individual.*',
'apostasy',
'tapostate',
'deserted',
r'deserter.*',
'deserting',
r'deceiv.*',
r'jilt.*',
'imposter',
'miscreant',
'spy',
'sequester',
'renegade',
r'terroris.*',
r'immigra.*',
r"abandon.*"]

authority_virtue = [r'obey.*',
r'obedien.*',
'duty',
'law',
r'lawful.*',
r'legal.*',
r'duti.*',
r'honor.*',
'respect',
r'respectful.*',
'respected',
'respects',
r'order.*',
r'father.*',
'mother',
r'motherl.*',
'mothering',
'mothers',
r'tradition.*',
r'hierarch.*',
r'authorit.*',
'permit',
'permission',
r'status.*',
r'rank.*',
r'leader.*',
'class',
'bourgeoisie',
r'caste.*',
'position',
r'complian.*',
'command',
'supremacy',
'control',
r'submi.*',
r'allegian.*',
'serve',
"preserve",
r'loyal.*']

authority_vice = [r'defian.*',
r'rebel.*',
r'dissent.*',
r'subver.*',
r'disrespect.*',
r'disobe.*',
r'sediti.*',
r'agitat.*',
r'insubordinat.*',
r'illegal.*',
r'lawless.*',
'insurgent',
'mutinous',
r'defy.*',
'dissident',
'unfaithful',
'alienate',
'defector',
r'heretic.*',
'nonconformist',
'oppose',
'protest',
'refuse',
'denounce',
'remonstrate',
r'riot.*',
'obstruct',
r'betray.*',
r'treason.*',
r'traitor.*',
r'treacher.*',
r'disloyal.*',
'apostasy',
'tapostate',
'deserted',
r'deserter.*',
'deserting']

purity_virtue = ['piety',
'pious',
'purity',
r'pure.*',
r'clean.*',
r'steril.*',
r'sacred.*',
r'chast.*',
'holy',
'holiness',
r'saint.*',
r'wholesome.*',
r'celiba.*',
'abstention',
'virgin',
'virgins',
'virginity',
'virginal',
'austerity',
'integrity',
'modesty',
r'abstinen.*',
'abstemiousness',
'upright',
'limpid',
'unadulterated',
'maiden',
'virtuous',
'refined',
r'decen.*',
'immaculate',
'innocent',
'pristine',
r'church.*',
"preserve"]

purity_vice = [r'disgust.*',
r'deprav.*',
r'disease.*',
r'unclean.*',
r'contagio.*',
r'indecen.*',
'sin',
r'sinful.*',
r'sinner.*',
'sins',
'sinned',
'sinning',
r'slut.*',
'whore',
r'dirt.*',
'impiety',
'impious',
r'profan.*',
'gross',
r'repuls.*',
r'sick.*',
r'promiscu.*',
r'lewd.*',
r'adulter.*',
r'debauche.*',
r'defile.*',
'tramp',
r'prostitut.*',
'unchaste',
'intemperate',
'wanton',
'profligate',
r'filth.*',
'trashy',
r'obscen.*',
'lax',
r'taint.*',
r'stain.*',
r'tarnish.*',
r'debase.*',
r'desecrat.*',
r'wicked.*',
'blemish',
r'exploitat.*',
'pervert',
r'wretched.*',
r"ruin.*",
"exploit",
"exploits",
"exploited",
"exploiting",
'apostasy',
'tapostate']

morality_general = [r'righteous.*',
r'moral.*',
r'ethic.*',
r'value.*',
'upstanding',
'good',
'goodness',
r'principle.*',
'blameless',
'exemplary',
'lesson',
'canon',
'doctrine',
'noble',
r'worth.*',
r'ideal.*',
'praiseworthy',
'commendable',
'character',
'proper',
'laudable',
'correct',
r'wrong.*',
'evil',
r'immoral.*',
'bad',
r'offend.*',
r'offensive.*',
r'transgress.*',
r'honest.*',
r'lawful.*',
r'legal.*',
'pious',
'purity',
'integrity',
r'wicked.*',
'upright',
r'decen.*',
r'indecen.*',
r'wretched.*',
r'wholesome.*']


list_of_categories = [harm_virtue, harm_vice, fairness_virtue, fairness_vice, 
                       ingroup_virtue, ingroup_vice, authority_virtue, authority_vice,
                       purity_virtue, purity_vice, morality_general]

## count frequencies in processed tweets, append each as column

apply_counter1 = 0

tweets_processed["frequencies"] = tweets_processed["Text_processed"].apply(
    compute_frequencies, list_of_categories=list_of_categories
)

harm_virtue_list2 = []
harm_vice_list2 = []
fairness_virtue_list2 = []
fairness_vice_list2 = []
authority_virtue_list2 = []
authority_vice_list2 = []
ingroup_virtue_list2 = []
ingroup_vice_list2 = []
purity_virtue_list2 = []
purity_vice_list2 = []
morality_general_list2 = []


list_of_categories2 = [harm_virtue_list2, harm_vice_list2, fairness_virtue_list2, fairness_vice_list2,
authority_virtue_list2, authority_vice_list2, ingroup_virtue_list2, ingroup_vice_list2,
purity_virtue_list2, purity_vice_list2, morality_general_list2]


for index, row in tweets_processed.iterrows():
    list_of_frequencies = row["frequencies"]

    for category, frequency in zip(list_of_categories2, list_of_frequencies):
        category += [frequency]

# ... and then we write each list to a column
list_of_category_names = ["harm_virtue", "harm_vice", "fairness_virtue", "fairness_vice",
                          "ingroup_virtue", "ingroup_vice", "authority_virtue", "authority_vice",
                          "purity_virtue", "purity_vice", "morality_general"]

for cat_name, cat_freqs in zip(list_of_category_names, list_of_categories2):
    tweets_processed[cat_name] = cat_freqs

del tweets_processed["frequencies"]

tweets_processed["harm_virtue"]


tweets_processed.head()

## export to csv


os.chdir("C:/Users/Alex/Desktop/Uni/Master Psychologie/WS 22/SE CSS/Final Project/project/data")

tweets_processed.to_csv("tweets_outcomes.csv")