import warnings
import sys
sys.path.append("..")
sys.path.insert(0, './app')
from app import util
from app.people import getPeoplesInfo1
from app.country_represent import country_present1
from app.util import highlight_json

from util import *
from app import util
from app.country_represent import country_represent
from app.similarity import retrieve_similar_question
from tabulate import tabulate
from app import db, metadata
import numpy as np
import torch
from transformers import BertTokenizer, BertForSequenceClassification
import sys
from flask import Flask, jsonify, request
from sklearn.feature_extraction.text import TfidfVectorizer
import click
from os import path
import json
import pickle
from collections import defaultdict
from typing import List, Optional, TYPE_CHECKING, Tuple
from flask import Blueprint, render_template, redirect
import tensorflow as tf


def warn(*args, **kwargs):
    pass


warnings.warn = warn
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)



# nltk.download('punkt') #Download once
func = Blueprint('func', __name__)

vectorizer, Matrix, ans = params[0], params[1], params[2]


def guess(question, max=12):
    answer = []
    repre = vectorizer.transform(question)
    matrix = Matrix.dot(repre.T).T
    indices = (-matrix).toarray().argsort(axis=1)[:, 0:max]
    for i in range(len(question)):
        answer.append([(ans[j], matrix[i, j]) for j in indices[i]])
    return answer[0][0:5]

# Cai End -------------------


@func.route("/act", methods=["POST"])
def act():
    if request.method == "POST":
        question = request.form.get("text")
        ans = request.form.get("answer_text")
    start = time.time()
    answer = guess(question=[question])
    # # Uncomment the below line to get the buzzer funtionality.
    # # get_importance_of_each_sentence(question)
    # # answer_sentence = guess_by_sentences(question)
    # difficulty = classify(question = [question])
    # ethnicity = find_ethnicity(answer)
    # gender = getGender(question)
    # similar_question = retrieve_similar_question(question)
    # country_representation = country_present(question)
    # # if(difficulty == "Hard"):
    
    # return jsonify({"guess": answer, "difficulty": difficulty, "ethnicity": ethnicity, "gender": gender, "similar_question": similar_question, "country_representation" : country_representation})
    
    # answer = tabulate(answer, tablefmt='html')
    # answer = "\n".join(str(x[0])+ " " + str(x[1]) for x in answer)
    answer = [{"guess": str(x[0]),"score":str(x[1])} for x in answer]
    end = time.time()
    # print(end - start)
    print("----TIME (s) : /func/act---", end - start)
    return jsonify({"guess": answer})


@func.route("/timeup", methods=["GET"])
def timeup():
    print("timeup")
    return "OK"


@func.route("country_people", methods=["POST"])
def country_people():
    if request.method == "POST":
        question = request.form.get("text")
    country_representation, countries = country_present1(question)
    highlight=highlight_json(countries)
    return jsonify({"country_representation": country_representation, "Highlight": highlight})

@func.route("/insert", methods=["POST"])
def insert():
    if request.method == "POST":
        question = request.form.get("text")
        ans = request.form.get("answer_text")
    print(question, ans)
    answer = guess(question=[question])
    qa_table = metadata.tables["qa"]
    db.session.execute(qa_table.insert().values(Question=question, Answer=ans))
    return "submitted"
{"mode":"full","isActive":False}