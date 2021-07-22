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
threshold_similar = 0.5
threshold_pronunciation = 0.6
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
    matrix = Matrix.dot(repre.T).T
    indices = (-matrix).toarray().argsort(axis=1)[:, 0:max]
    for i in range(len(question)):
        answer.append([(ans[j], matrix[i, j]) for j in indices[i]])
    return answer[0][0:n]

def load_bert_model():
    model = BertForSequenceClassification.from_pretrained(
        './model/difficulty_models/BERT_full_question')
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    return model, tokenizer


def highlight_json(items = None, color = None):
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
    for item in items:
        temp = {}
        temp['text'] = item
        temp['style'] = "background-color:"+color
        highlight.append(temp)
    return highlight



model, tokenizer = load_bert_model()
params = get_pretrained_tfidf_vectorizer()

def load_genre_model():
    model = BertForSequenceClassification.from_pretrained('./model/genre_classifier_models/BERT_genre_classifier', num_labels = 11)
    # tokenizer = BertTokenizer.from_pretrained('bert-base-uncased') 
    return model

# genre_model = load_genre_model()

def load_science_genre_model():
    model = BertForSequenceClassification.from_pretrained('./model/genre_classifier_models/Science_Genre_classifier', num_labels = 4)
    return model

# science_genre_model = load_science_genre_model()
sub_genres = {
            'Philosophy': [['Norse', 354], ['Other', 345], ['Philosophy', 5], ['European', 3], ['American', 2], ['Religion/Mythology', 1]],
            'History' : [['American', 3514], ['World', 3103], ['European', 3100], ['British', 685], ['Classical', 607], ['Ancient', 345], ['Other', 541], ['Classic', 105], ['Norse', 48], ['Geography', 2], ['Religion/Mythology', 1]],
            'Literature': [[ 'American', 3463], ['European', 3194], ['British', 2052], ['World', 1934], ['Europe', 421],  ['Other', 629], ['Classical', 249], ['Classic', 58], ['Norse', 40], ['Language Arts', 19], ['Religion/Mythology', 1], ['Pop Culture', 1], ['Art', 1]],
            'Mythology': [[ 'Norse', 365], ['Religion/Mythology', 15], ['American', 6], ['Greco-Roman', 2], ['Earth Science', 1], ['Japanese', 1], ['Music', 1]],
            'Current Events' : [['None', 362]],
            'Religion': [['Norse', 318], ['Religion/Mythology', 6], ['Other', 377], ['American', 3], ['East Asian', 2], ['Ancient', 1], ['World', 1]],
            'Trash' : [['Pop Culture', 349], ['Norse', 313], ['Other', 545], ['American', 5], ['World', 1], ['Movies', 1], ['Classic', 1]],
            'Social Science': [['Religion/Mythology', 1017], ['Philosophy', 540], ['Geography', 480], ['None', 322], ['Psychology', 203], ['Economics', 172], ['Anthropology', 154], ['Norse', 100],  ['Other', 77], ['World', 1], ['Language Arts', 1], ['American', 1], ['European', 1]],
            'Science': [['Biology', 2727], ['Physics', 2413], ['Chemistry', 2281], ['Math', 1268], ['Other', 1523], ['Computer Science', 297], ['Astronomy', 204], ['Earth Science', 157], ['Norse', 71], ['Religion/Mythology', 1], ['Psychology', 1], ['Pop Culture', 1], ['World', 1]],
            'Fine Arts': [['Visual', 1980], ['Auditory', 1233], ['Other', 1400], ['Music', 1039], ['Audiovisual', 769], ['Art', 587], ['Norse', 7], ['American', 2]],
            'Geography': [['Norse', 238], ['Other', 287], ['Geography', 15], ['World', 3], ['American', 1]]

        }
genres = ['Philosophy', 'History', 'Literature', 'Mythology', 'Current Events', 'Religion', 'Trash', 'Social Science', 'Science', 'Fine Arts', 'Geography']



