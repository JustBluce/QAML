# Cai Start -------------------
def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn
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

sys.path.append("..")
sys.path.insert(0, 'C:/Users/rajsa/Desktop/qanta-codalab-master/TryoutProject/Flask/app')

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
    return jsonify({"guess": answer})
