# Atith
# <<<-------DEPRECIATED FILE-------->>>
# Description of this file: 
# 1. Contains code for the genre classifier: Pie chart on the front end
def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn
from flask import Blueprint, render_template, redirect
from flask import Flask, jsonify, request
from app import db, metadata
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from flask import Flask, jsonify, request
import sys
import torch
import sys
sys.path.append("..")
sys.path.insert(0, './app')

from app import util, importance
from util import *
from importance import *

sci_genres = ['Biology', 'Chemistry', 'Physics', 'Math']

def science_genre_classify(question):
    
    start = time.time()

    # inputs = tokenizer(question, return_tensors="pt")
    # outputs = science_genre_model(**inputs)
    # logits = outputs.logits.detach().cpu().numpy()
    # genre_index = np.argmax(logits).flatten()
    end = time.time()
    print("----TIME (s) : /genre_classifier/classify [sub-genre]---",end - start)
    # if(difficulty == 0):
    #     return jsonify({"difficulty": "Easy"})
    # elif (difficulty == 1):
    #     return jsonify({"difficulty": "Hard"})
    return sci_genres[genre_index[0]]
    
    
    