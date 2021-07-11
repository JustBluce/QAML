# Atith
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
import subgenre_classifier
sys.path.append("..")
sys.path.insert(0, './app')

from app import util, importance
from util import *
from importance import *

genres = ['Philosophy', 'History', 'Literature', 'Mythology', 'Current Events', 'Religion', 'Trash', 'Social Science', 'Science', 'Fine Arts', 'Geography']
genre_classifier = Blueprint('genre_classifier', __name__)
@genre_classifier.route("/classify", methods=["POST"])
def classify():
    if request.method == "POST":
        question = request.form.get("text")
    start = time.time()

    inputs = tokenizer(question, return_tensors="pt")
    outputs = genre_model(**inputs)
    logits = outputs.logits.detach().cpu().numpy()
    genre_index = np.argmax(logits).flatten()
    end = time.time()
    print("----TIME (s) : /genre_classifier/classify---",end - start)
    # if(difficulty == 0):
    #     return jsonify({"difficulty": "Easy"})
    # elif (difficulty == 1):
    #     return jsonify({"difficulty": "Hard"})
    print(genres[genre_index[0]])
    subgenre = None
    if(genres[genre_index[0]] == 'Science'):
        subgenre = subgenre_classifier.science_genre_classify(question)
    print(subgenre)
    return jsonify({"genre": genres[genre_index[0]], "subgenre": subgenre})
    