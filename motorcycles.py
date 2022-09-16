#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  3 10:39:25 2022

@author: meghanadkayanattil
"""

import psaw
import datetime as dt
import pandas as pd
import random

from transformers import AutoTokenizer, pipeline
t = AutoTokenizer.from_pretrained("bhadresh-savani/bert-base-go-emotion")
model = "bhadresh-savani/bert-base-go-emotion"

class motorcycles:

    global all_comments 
    
    def __init__(self, name, subred, begenning, ending):
        self.name = name
        self.subred = subred
        self.begenning = begenning
        self.ending = ending

    def get_comments(self):
        # Using the psaw api to get comments containing the string 'self.name'
        api = psaw.PushshiftAPI()
        current_epoch = int(dt.datetime(
            self.begenning.year, self.begenning.month, self.begenning.day).timestamp()) # time stamp creation of the current day
        old_epoch = int(dt.datetime(self.ending.year,
                        self.ending.month, self.ending.day).timestamp()) # time stamp creation of the ending day
        try:
            comments = api.search_comments(q=self.name, subreddit=self.subred,
                                           limit=100000, before=current_epoch,
                                           after=old_epoch) # get all the texts and details
        except:
            return [], [], [] # som time the psaw api outputs that the servers are down in that case we 
            # return null values so that the app.py can  accordingly handle errors

        comments_dict = {'Text': [], 'User ID': [], 'Score(upvotes-downvotes)': [],
                         'Date of the comment': []} 

        for comment in comments: # converting the scraped data into a dictionary
            date = dt.datetime.fromtimestamp(comment.created_utc)
            if self.name in comment.body:
                comments_dict['Text'].append(comment.body)
                comments_dict['User ID'].append(comment.id)
                comments_dict['Score(upvotes-downvotes)'].append(comment.score)
                comments_dict['Date of the comment'].append(date)

        # df = pd.DataFrame(comments_dict) # converting the dictionary into a dataframe
        # df.drop_duplicates(subset=['Text'], keep='last', inplace=True) # removing duplicate comments
        all_comments = comments_dict["Text"] # df.Text

        if len(all_comments) == 0: # sometimes the search string does not match exactly the name input
            # then we return null values so that the app.py can  accordingly handle errors
            print("No data found")
            return [], [], []

        rand_i = random.randint(0, len(all_comments))
        example_comment = all_comments[rand_i] # chosing a random comment to display later
        return example_comment, len(all_comments), all_comments

def analysis_huggingface(all_comments):    
    short_comments = []
    for comment in all_comments:
        if len(comment)<512:
            short_comments.append(comment)
        
    classifier = pipeline('sentiment-analysis', model,  tokenizer=t)
    results = classifier(short_comments)
    sentiment = pd.DataFrame(results)
    sentiment_label = sentiment.label.value_counts()[:10].index.tolist()
    sentiment_count = sentiment.label.value_counts()[:10].tolist()
    print(short_comments[2])
    return sentiment_label, sentiment_count

# %% 
#  TEST

# bikename = 'interceptor'
# subred_name = 'motorcycle'
# current, begenning = hf.time_frame_calculator('Last 1 year')
# moto = motorcycles(bikename, subred_name, current, begenning)
# _,_,all_comm = moto.get_comments()
# analysis_huggingface(all_comm)
