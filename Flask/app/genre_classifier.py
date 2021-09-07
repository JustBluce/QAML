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
import subgenre_classifier
sys.path.append("..")
sys.path.insert(0, './app')

from app import util, importance
from util import *


genre_classifier = Blueprint('genre_classifier', __name__)
@genre_classifier.route("/classify", methods=["POST"])
def classify():
    if request.method == "POST":
        question = request.form.get("text")
    start = time.time()

    # inputs = tokenizer(question, return_tensors="pt")
    # outputs = genre_model(**inputs)
    # logits = outputs.logits.detach().cpu().numpy()
    # genre_index = np.argmax(logits).flatten()
    end = time.time()
    print("----TIME (s) : /genre_classifier/classify [genre]---",end - start)
    # if(difficulty == 0):
    #     return jsonify({"difficulty": "Easy"})
    # elif (difficulty == 1):
    #     return jsonify({"difficulty": "Hard"})
    # print(genres[genre_index[0]])
    # subgenre = None
    # if(genres[genre_index[0]] == 'Science'):
    #     subgenre = subgenre_classifier.science_genre_classify(question)
    # print(subgenre)
    # return jsonify({"genre": genres[genre_index[0]], "subgenre": subgenre})
    return jsonify({ "subgenre": sub_genres})
    
@genre_classifier.route("/genre_data", methods=["POST"])
def genre_data():
    if request.method == "POST":
        question = request.form.get("text")
        u_id = request.form.get("user_id")

    # print(u_id)
    start = time.time()
    if u_id is None:
        u_id = '0'
    sql="SELECT Genre, count(*) from QA.Question  where UserId LIKE \'" + u_id  + "\' group by Genre"
    result_sql = []
    try:
        result_sql = db.session.execute(sql)
        result_sql = result_sql.fetchall()
        db.session.commit()
    except:
        db.session.rollback()

    result=[]
    for instance in result_sql:
        
        temp = []
        temp.append(instance[0])
        temp.append(instance[1])
        result.append(temp)

    sql="SELECT Question, Answer, Genre, Point from QA.Question  where UserId LIKE \'" + u_id  + "\' "
    result_sql = []
    try:
        result_sql = db.session.execute(sql)
        result_sql = result_sql.fetchall()
        db.session.commit()
    except:
        db.session.rollback()

    questions_list=[]
    for instance in result_sql:
        
        temp = {}
        temp['Question'] = instance[0]
        temp['Answer'] = instance[1]
        temp['Genre'] = instance[2]
        temp['Point'] = instance[3]
        questions_list.append(temp)

    print(result)
    end = time.time()
    print("----TIME (s) : /genre_classifier/genre_data [genre]---",end - start)
    return jsonify({ "genre_data": result, "questions_list": questions_list})
    
    