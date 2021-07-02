def warn(*args, **kwargs):
    pass
threshold = 0.5
import warnings
import nltk
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