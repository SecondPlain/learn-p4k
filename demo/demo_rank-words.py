# -*- coding: utf-8 -*-
"""
Created on Wed Jan 14 20:46:06 2015

@author: Jonathan D. Jones
"""

import os
import numpy as np
import json
from collections import defaultdict
import re
import operator

# Root directory of the learn-p4k repository.
# CHANGE THIS so it's the correct path on your computer.
root_dir = '/home/jdjones/repo/learn-p4k/'

# Load pitchfork review corpus as a list of dictionaries
# Each list entry is a dictionary with the following keys (all values are 
# string lists):
#   artist: Album artist. Multiple artists separated by ' / '.
#   title: Album title.
#   label: Record label that released album. Multiple labels separated by ' / '.
#   year: Release year. Multiple years separated by '/' (no spaces).
#   author: Review author. Multiple authors separated by ' & ' (?).
#   score: Album score.
#   bnm_label: Best New Music/Reissue label.
#   date: Date of review, of format Month Day, Year
#   review: Review text.
p4k_dir = os.path.join(root_dir, 'data', 'p4k')
p4k_file = open(os.path.join(p4k_dir, 'p4k-all.json'))
p4k_data = json.load(p4k_file)
p4k_file.close()

# Map scores to words
word_scores = defaultdict(list)
for i in range(len(p4k_data)):
    
    # Read in review and all meta-data
    cur_item = p4k_data[i]
    cur_review = cur_item["review"][0]
    cur_artists = cur_item["artist"]
    cur_titles = cur_item["title"]
    cur_labels = cur_item["label"]
    cur_scores = cur_item["score"]
    cur_bnm_labels = cur_item["bnm_label"]
    cur_dates = cur_item["date"]
    
    # Cast scores to float
    for j in range(len(cur_scores)):
        cur_scores[j] = float(cur_scores[j])
    
    # Convert non-alphanumeric characters to whitespace, convert to lowercase,
    # map scores to words
    # Following line is for python 2.7
    # cur_review = re.sub(ur"[^ a-z0-9]", " ", cur_review.lower())
    cur_review = re.sub(r"[^ a-z0-9]", " ", cur_review.lower())
    words = cur_review.split()
    for cur_word in words:
        word_scores[cur_word] += cur_scores

# Calculate word rank
# TODO: Rank by Bayesian average
word_ranks = defaultdict(int)
for word, scores in word_scores.items():
    word_ranks[word] = np.mean(scores)

# Write words to file in order of rank
top_words = sorted(word_ranks.items(), key=operator.itemgetter(1))
top_words.reverse()     # ascending by default
out_dir = os.path.join(root_dir, 'data', 'output')
# Line below: 'wb' for python 3.x
out_handle = open(os.path.join(out_dir, 'ranked-words.txt'), 'wb')
for word, rank in top_words:
    num_scores = len(word_scores[word])
    out_str = '{0:.3}\t{1}\t{2}\n'.format(rank, num_scores, word)
    out_handle.write(out_str.encode('utf8'))
out_handle.close()