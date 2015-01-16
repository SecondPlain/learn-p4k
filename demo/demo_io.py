# -*- coding: utf-8 -*-
"""
Created on Fri Jan  9 18:55:29 2015

@author: Jonathan D. Jones
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import json
from collections import defaultdict
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

# Extract score, caculate average score per record label
scores = []
avg_label_scores = defaultdict(int)
num_label_scores = defaultdict(int)
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
    
    # Calculate each record label's average score
    for j in range(len(cur_scores)):
        score = float(cur_scores[j])
        scores.append(score)
        labels = cur_labels[j].split(' / ')
        for label in labels:
            prev_total = avg_label_scores[label] * num_label_scores[label]
            num_label_scores[label] += 1.0
            avg_label_scores[label] = (prev_total + score) / num_label_scores[label]

# Plot histogram of review scores    
score_hist = np.zeros((101,1))
for score in scores:
    idx = int(score*10)
    score_hist[idx] += 1
plt.plot(score_hist)
plt.title('Histogram of review scores')
plt.ylabel('Count')
plt.xlabel('Score (x10)')
plt.show()

# Sort record labels by number of reviews (descending) and print the top 100
most_reviews = sorted(num_label_scores.items(), key=operator.itemgetter(1))
most_reviews.reverse()  # sorted is ascending by default
top_label_scores = {}
for i in range(100):
    cur_label, num_reviews = most_reviews[i]
    top_label_scores[cur_label] = avg_label_scores[cur_label]    
best_scores = sorted(top_label_scores.items(), key=operator.itemgetter(1))
best_scores.reverse()   # sorted is ascending by default
print("100 most-reviewed labels, ranked by average score:")
for i in range(100):
    cur_label, cur_score = best_scores[i]
    out_str = '{0:.3}\t{1}'.format(cur_score, cur_label)
    print(out_str) 