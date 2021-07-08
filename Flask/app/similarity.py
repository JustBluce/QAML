from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity 
import nltk
from nltk.corpus import stopwords
import json
import numpy as np
import en_core_web_sm
from flask import Blueprint, render_template, redirect
from flask import Flask, jsonify, request
nlp = en_core_web_sm.load()

stopWords = stopwords.words('english')

f = open('app/qanta.json')
data = json.load(f)['questions']


questions = []

for i in range(0, len(data)):
    questions.append(data[i]['text'])

similar_question = Blueprint('similar_question', __name__)
@similar_question.route("/retrieve_similar_question", methods=["POST"])
def retrieve_similar_question():
    
    if request.method == "POST":
        question = request.form.get("text")
    questions.append(question)
    tfidf_vectorizer = TfidfVectorizer(stop_words = stopWords)
    tfidf_matrix = tfidf_vectorizer.fit_transform(questions)
    cosine = cosine_similarity(tfidf_matrix[len(questions)-1], tfidf_matrix)[0]
    max_cosine = max(cosine[:len(questions)-1])
    print(max_cosine)

    max_index = np.where(cosine == max_cosine)
    print([max_cosine, questions[max_index[0][0]]])
    isSimilar = False
    if max_cosine > 0.1:
        isSimilar = True
    return jsonify({"similar_question": [isSimilar, questions[max_index[0][0]]]})