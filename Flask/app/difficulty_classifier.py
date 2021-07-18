# Atith
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
sys.path.append("..")
sys.path.insert(0, './app')

from app import util, importance
from util import *
from importance import *

difficulty_classifier = Blueprint('difficulty_classifier', __name__)
@difficulty_classifier.route("/classify", methods=["POST"])
def classify():
    if request.method == "POST":
        question = request.form.get("text")
    start = time.time()

    inputs = tokenizer(question, return_tensors="pt")
    outputs = model(**inputs)
    logits = outputs.logits.detach().cpu().numpy()
    difficulty = np.argmax(logits).flatten()
    end = time.time()
    print("----TIME (s) : /difficulty_classifier/classify---",end - start)
    if(difficulty == 0):
        return jsonify({"difficulty": "Easy"})
    elif (difficulty == 1):
        return jsonify({"difficulty": "Hard"})

    return jsonify({"difficulty": "error"})
    