"""
Created on Jan 14

@author: Jonathan Jones & Kathleen Kusworo
"""

import numpy as np
import matplotlib.pyplot as plt
import json
from collections import defaultdict
import operator
import re
import random
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn import svm
from sklearn.svm import LinearSVC

def binarize(scores, mean):
    for i in range(len(scores)):
        if scores[i] >= mean:
            scores[i] = 1
        else:
            scores[i] = -1

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
p4k_dir = '/home/jdjones/repo/learn-p4k/data/p4k/'
p4k_file = open(p4k_dir + 'p4k-all.json')
p4k_data = json.load(p4k_file)

test_dev_int = []
train_int = []
train = []
train_score = []
test_score = []
dev_score = []
test_int = []
dev_int = []
test = []
dev = []

'''
# Read in review and all meta-data
for i in range(len(p4k_data)):    
    
    cur_item = p4k_data[i]

    #replace dashesa and periods in reviews with empty spaces, then split by space
    #cur_review = cur_item["review"][0].replace("-"," ").replace("."," ").split(" ")

    #go through the list of words and remove any non-alphanumeric characters
    #for j in range(len(cur_review)):
    #    cur_review[j] = re.sub(r'\W+', '', cur_review[j])

    #remove any resulting empty strings
    #while '' in cur_review:
    #    cur_review.remove('')   

    #assign the formatted review back to p4k_data
    p4k_data[i]["review"] = cur_review

    cur_artists = cur_item["artist"]
    cur_titles = cur_item["title"]
    cur_labels = cur_item["label"]
    cur_scores = cur_item["score"]
    cur_bnm_labels = cur_item["bnm_label"]
    cur_dates = cur_item["date"]
    
'''

#pick ~5361 unique integers randomly from 0-16082
test_dev_int = random.sample(range(len(p4k_data)), int(len(p4k_data)/5))

#set the rest to be train integers
train_int = set(range(len(p4k_data))) - set(test_dev_int)
train_int = list(train_int)
train_int = random.sample(train_int, int(len(train_int)*3/8))

#assign the first half as integers for the test set
for i in range(int(len(test_dev_int)/2)):
    test_int.append(test_dev_int[i])

#assign the second half as integers for the dev set
for i in range(int(len(test_dev_int)/2), len(test_dev_int)):
    dev_int.append(test_dev_int[i])

#assign corpus items that are numbered as the integers in test_int into test
for i in range(len(test_int)):
    cur_item = p4k_data[test_int[i]]  
    scores = cur_item["score"]
    if scores:    
        for j in range(len(scores)):
            scores[j] = float(scores[j])
        test.append(cur_item["review"][0])
        test_score.append(np.mean(scores))
    else:
        print("Skipping review: no score")

#assign corpus items that are numbered as the integers in dev_int into dev
for i in range(len(dev_int)):
    cur_item = p4k_data[dev_int[i]]  
    scores = cur_item["score"]
    if scores:    
        for j in range(len(scores)):
            scores[j] = float(scores[j])
        dev.append(cur_item["review"][0])
        dev_score.append(np.mean(scores))
    else:
        print("Skipping review: no score")

#assign reviews of corpus items that are numbered as the integers in train_int into train
for i in range(len(train_int)):
    #current item is the item in p4k_data numbered as those selected to be in train set
    cur_item = p4k_data[train_int[i]]  
    scores = cur_item["score"]
    if scores:    
        for j in range(len(scores)):
            scores[j] = float(scores[j])
        train.append(cur_item["review"][0])
        train_score.append(np.mean(scores))
    else:
        print("Skipping review: no score")

avg = np.mean(train_score)
binarize(train_score, avg)
binarize(dev_score, avg)
binarize(test_score, avg)
        
vectorizer = HashingVectorizer(stop_words='english', non_negative = True)
X_train = vectorizer.fit_transform(train)
X_dev = vectorizer.fit_transform(dev)

classifier = LinearSVC(penalty="l1",dual=False, tol=1e-3)
classifier.fit(X_train,train_score)
output = classifier.predict(X_dev)

num_correct = 0.0

for i in range(len(dev_score)):
    if dev_score[i] == output[i]:
        num_correct += 1
        
accuracy = num_correct / len(dev_score)        

print(accuracy)
