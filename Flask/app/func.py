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
from transformers import BertTokenizer, BertForSequenceClassification
import torch
import numpy as np
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
    print(answer[0][0][0])
    return answer[0][0][0]

#classify function was written by Atith Gandhi
def classify(question):
    model = BertForSequenceClassification.from_pretrained('./model/difficulty_models/BERT_full_question')
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased') 

    inputs = tokenizer(question, return_tensors="pt")
    outputs = model(**inputs)
    logits = outputs.logits.detach().cpu().numpy()
    difficulty = np.argmax(logits).flatten()
    print(difficulty)
    if(difficulty == 0):
        return 'Easy'
    elif (difficulty == 1):
        return 'Hard'


@func.route('/act', methods=['POST'])
def act():
    if request.method == 'POST':
        question = request.form.get('text')
    answer = guess(question=[question])
    difficulty = classify(question = [question])
    if(difficulty == "Hard"):
        sql = "insert into QA (Question, Answer) VALUES ('"+question+"', '"+answer +"'); "
        result_sql=db.session.execute(sql)

    return jsonify({'guess': answer, "difficulty": difficulty})
