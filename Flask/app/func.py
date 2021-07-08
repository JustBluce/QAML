# Cai Start -------------------
import nltk
from app import db, metadata
import numpy as np
import torch
from transformers import BertTokenizer, BertForSequenceClassification
import sys
from flask import Flask, jsonify, request
from sklearn.feature_extraction.text import TfidfVectorizer
import click
import os
import json
import pickle
from collections import defaultdict
from typing import List, Optional, Tuple
from flask import Blueprint, render_template, redirect
import warnings


def warn(*args, **kwargs):
    pass


threshold = 0.4
warnings.warn = warn

from app.similarity import retrieve_similar_question
from app.country_represent import country_represent

sys.path.append("..")
sys.path.insert(0, os.path.dirname(__file__))

from app import util
from util import *

import nltk
# nltk.download('punkt') #Download once
func = Blueprint('func', __name__)



def guess(question, max=12):
    vectorizer, Matrix, ans = get_pretrained_tfidf_vectorizer()
    answer = []
    repre = vectorizer.transform(question)
    matrix = Matrix.dot(repre.T).T
    indices = (-matrix).toarray().argsort(axis=1)[:, 0:max]
    for i in range(len(question)):
        answer.append([(ans[j], matrix[i, j]) for j in indices[i]])
    return answer[0][0][0]

# Cai End -------------------

#classify function was written by Atith Gandhi
    

@func.route("/act", methods=["POST"])
def act():
    if request.method == "POST":
        question = request.form.get("text")
    answer = guess(question=[question])
    # Uncomment the below line to get the buzzer funtionality.
    # get_importance_of_each_sentence(question)
    # answer_sentence = guess_by_sentences(question)
    # difficulty = classify(question=[question])
    # if(difficulty == "Hard"):
    #     qa_table = metadata.tables["QA"]
    #     db.session.execute(qa_table.insert().values(
    #         Question=question, Answer=answer))

    # answer = guess(question=[question])
    # # Uncomment the below line to get the buzzer funtionality.
    # # get_importance_of_each_sentence(question)  
    # # answer_sentence = guess_by_sentences(question)
    # difficulty = classify(question = [question])
    # ethnicity = find_ethnicity(answer)
    # gender = getGender(question)
    # similar_question = retrieve_similar_question(question)
    # country_representation = country_present(question)
    # # if(difficulty == "Hard"):
    # #     qa_table = metadata.tables["QA"]
    # #     db.session.execute(qa_table.insert().values(Question=question, Answer=answer))
    # return jsonify({"guess": answer, "difficulty": difficulty, "ethnicity": ethnicity, "gender": gender, "similar_question": similar_question, "country_representation" : country_representation})


    # answer = guess(question=[question])
    return jsonify({"guess": answer})


@func.route("/timeup", methods=["GET"])
def timeup():
    print("timeup")
    return "OK"
