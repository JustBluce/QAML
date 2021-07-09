def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn
import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
from flask import Blueprint, render_template, redirect
from typing import List, Optional, TYPE_CHECKING, Tuple
from collections import defaultdict
import pickle
import json
from os import path
import click
from sklearn.feature_extraction.text import TfidfVectorizer
from flask import Flask, jsonify, request
import sys
from transformers import BertTokenizer, BertForSequenceClassification
import torch
import numpy as np
from app import db, metadata
from tabulate import tabulate
from app.similarity import retrieve_similar_question
from app.country_represent import country_represent
sys.path.append("..")
sys.path.insert(0, './app')

from app import util
from util import *

import nltk
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
    start = time.time()
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
    answer = guess(question=[question])
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