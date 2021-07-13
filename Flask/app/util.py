from transformers import BertTokenizer, BertForSequenceClassification
import time
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
import nltk
import warnings
import os


def warn(*args, **kwargs):
    pass
threshold_buzz = 0.2
threshold_similar = 0.3
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import warnings
import nltk
warnings.filterwarnings('ignore')


def colored(r, g, b, text):
    return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255".format(r, g, b, text)


def break_into_sentences(question):
    array_of_sentences_in_question = nltk.tokenize.sent_tokenize(question)
    return array_of_sentences_in_question


def break_into_words(question):
    array_of_words = question.split(' ')
    return array_of_words


def get_pretrained_tfidf_vectorizer():
    with open("./model/model.pickle", "rb") as f:
        params = pickle.load(f)

    vectorizer = params["tfidf_vectorizer"]
    Matrix = params["tfidf_matrix"]
    ans = params["i_to_ans"]
    return vectorizer, Matrix, ans


def guess_top_n(question, params, max=12, n=3):
    vectorizer, Matrix, ans = params[0], params[1], params[2]
    answer = []
    repre = vectorizer.transform(question)
    # print(repre.shape)

    matrix = Matrix.dot(repre.T).T
    indices = (-matrix).toarray().argsort(axis=1)[:, 0:max]
    for i in range(len(question)):
        answer.append([(ans[j], matrix[i, j]) for j in indices[i]])
    # print(answer)
    return answer[0][0:n]


def load_bert_model():
    model = BertForSequenceClassification.from_pretrained(
        './model/difficulty_models/BERT_full_question')
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    return model, tokenizer


def highlight_json(countries, people = None):
    '''
    Organize the json structure for text highlighting in frontend
    highlight: [
        { text: "American", style: "background-color:#f37373" },
        { text: "India", style: "background-color:#f37373" },
        { text: "Jack", style: "background-color:#fff05e" },
        { text: "Mary", style: "background-color:#fff05e" },
      ],
    '''
    highlight = []
    for country in countries:
        temp = {}
        temp['text'] = country
        temp['style'] = "background-color:#f37373"
        highlight.append(temp)
    # for person in people:
    #     temp = {}
    #     temp['text'] = person
    #     temp['style'] = "background-color:#fff05e"
    #     highlight.append(temp)

    return highlight


model, tokenizer = load_bert_model()
params = get_pretrained_tfidf_vectorizer()

def load_genre_model():
    model = BertForSequenceClassification.from_pretrained('./model/genre_classifier_models/BERT_genre_classifier', num_labels = 11)
    # tokenizer = BertTokenizer.from_pretrained('bert-base-uncased') 
    return model

genre_model = load_genre_model()

def load_science_genre_model():
    model = BertForSequenceClassification.from_pretrained('./model/genre_classifier_models/Science_Genre_classifier', num_labels = 4)
    return model

science_genre_model = load_science_genre_model()

