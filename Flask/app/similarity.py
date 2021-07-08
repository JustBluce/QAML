import sys
sys.path.append("..")
sys.path.insert(0, './app')

from app import util, importance
from util import *
from importance import *
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity 
import nltk
from nltk.corpus import stopwords
import json
import numpy as np
import spacy
## import en_core_web_sm
from flask import Blueprint, render_template, redirect
from flask import Flask, jsonify, request
nlp = spacy.load("en_core_web_sm")
##nlp = en_core_web_sm.load()

stopWords = stopwords.words('english')

f = open('app/qanta.json')
data = json.load(f)['questions']


questions = []

for i in range(0, len(data)):
    questions.append(data[i]['text'])
tfidf_vectorizer = TfidfVectorizer(stop_words = stopWords)
tfidf_matrix = tfidf_vectorizer.fit_transform(questions)



similar_question = Blueprint('similar_question', __name__)
@similar_question.route("/retrieve_similar_question", methods=["POST"])
def retrieve_similar_question():
    
    if request.method == "POST":
        question = request.form.get("text")
    start =time.time()
    questions.append(question)
    repre = tfidf_vectorizer.transform([question])
    matrix = tfidf_matrix.dot(repre.T).T
    matrix = matrix.toarray()
    # cosine = cosine_similarity(tfidf_matrix[len(questions)-1], tfidf_matrix)[0]
    max_cosine = max(matrix[0])
    # print(matrix)

    max_index = np.where(matrix == max_cosine)
    # print([max_cosine, questions[max_index[0][0]]])
    isSimilar = False
    if max_cosine > threshold:
        isSimilar = True
    end = time.time()
    print("----TIME (s) : /similar_question/retrieve_similar_question---",end - start)
    return jsonify({"similar_question": [isSimilar, questions[max_index[0][0]]]})