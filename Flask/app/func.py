from flask import Blueprint, render_template, redirect
from typing import List, Optional, Tuple
from collections import defaultdict
import pickle
import json
from os import path
import click
from sklearn.feature_extraction.text import TfidfVectorizer
from flask import Flask, jsonify, request
import sys
from app import db
sys.path.append("..")

func = Blueprint('func', __name__)

with open('./model/model.pickle', 'rb') as f:
    params = pickle.load(f)

vectorizer = params['tfidf_vectorizer']
Matrix = params['tfidf_matrix']
ans = params['i_to_ans']


def guess(question, max=12):
    answer = []
    repre = vectorizer.transform(question)
    matrix = Matrix.dot(repre.T).T
    indices = (-matrix).toarray().argsort(axis=1)[:, 0:max]
    for i in range(len(question)):
        idx = indices[i]
        answer.append([(ans[j], matrix[i, j]) for j in idx])
    return answer[0][0][0]


@func.route('/act', methods=['POST'])
def act():
    if request.method == 'POST':
        question = request.form.get('text')
    answer = guess(question=[question])

    sql = "insert into QA (Question, Answer) VALUES ('"+question+"', '"+answer +"'); "
    result_sql=db.session.execute(sql)

    return jsonify({'guess': answer})
