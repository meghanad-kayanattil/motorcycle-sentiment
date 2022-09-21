#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  3 10:39:25 2022

@author: meghanadkayanattil
"""

import psaw
import datetime as dt
import random
from transformers import AutoTokenizer, pipeline
t = AutoTokenizer.from_pretrained("arpanghoshal/EmoRoBERTa")

model = "arpanghoshal/EmoRoBERTa"
classifier = pipeline('sentiment-analysis', model,  tokenizer=t)

def get_comments_and_analyze(name, subred, begenning, ending):

    # Using the psaw api to get comments containing the string 'self.name'
    api = psaw.PushshiftAPI()
    current_epoch = int(dt.datetime(begenning.year, begenning.month, begenning.day).timestamp()) # time stamp creation of the current day
    old_epoch = int(dt.datetime(ending.year, ending.month, ending.day).timestamp()) # time stamp creation of the ending day
    try:
        comments = api.search_comments(q=name, subreddit=subred,
                                           limit=100000, before=current_epoch,
                                           after=old_epoch) # get all the texts and details
        labels = []
        all_comments = []
   
        for comment in comments:
            if (len(comment.body)<512) and ((name in comment.body) or (name.lower() in comment.body)): 
                result = classifier(comment.body)
                labels.append(result[0]['label'])
                all_comments.append(comment.body)
            

        counts = {i:labels.count(i) for i in labels}
        sentiment_label = counts.keys()
        sentiment_count = counts.values()
        len_coms = len(all_comments)
        rand_i = random.randint(0, len_coms)
        example_comment = all_comments[rand_i]

        return example_comment, len_coms, sentiment_label, sentiment_count 
    except:
        return [], [], [], [] # som time the psaw api outputs that the servers are down in that case we 
            # return null values so that the app.py can  accordingly handle errors

# %% 
#  TEST
#import helper_functions as hf
#bikename = 'interceptor'
#subred_name = 'motorcycle'
#current, begenning = hf.time_frame_calculator('Last 1 year')
#_,_,_,senti = get_comments(bikename, subred_name, current, begenning)
#print(senti)
# %%
