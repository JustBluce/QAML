
def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn
from flask import Blueprint, render_template, redirect
from flask import Flask, jsonify, request
from app import db, metadata
import sys
sys.path.append("..")
sys.path.insert(0, 'C:/Users/rajsa/Desktop/qanta-codalab-master/TryoutProject/Flask/app')

from app import util, importance
from util import *
from importance import *

binary_search_based_buzzer = Blueprint('binary_search_based_buzzer', __name__)

def buzz(question):
    answer = []
    temp_word_array = break_into_words(question)
    # print(temp_word_array)
    # check if buzzer ever goes above threshold
    index_of_bin_search = len(temp_word_array)
    question_sentence = " ".join(temp_word_array[:index_of_bin_search])
    temp_var = guess_top_5(question = [question_sentence])
    if (temp_var[0][1]>threshold):
        print("Buzzer rings on full question")
    else:
        print("Buzzer never crosses the threshold")
        return "Buzzer never crosses the threshold"
    store_index = index_of_bin_search
    min_index = 5
    max_index = len(temp_word_array) -1
    while max_index >= min_index:
        # print("inside while")
        # print(max_index, min_index, index_of_bin_search)
        index_of_bin_search =(max_index+min_index)//2
        question_sentence = " ".join(temp_word_array[:index_of_bin_search])
        temp_var = guess_top_5(question = [question_sentence])
        if (temp_var[0][1]>threshold):
            max_index = index_of_bin_search-1
            store_index = index_of_bin_search
        else:
            min_index = index_of_bin_search+1
    print("Index is :" + str(store_index) + " score is " + str(temp_var[0][1]) + " with guess = " + str(temp_var[0][0]) )    
    print(" ".join(temp_word_array[:store_index])+"||BUZZ||")
    return " ".join(temp_word_array[:store_index])+"||BUZZ||"

@binary_search_based_buzzer.route("/buzz_full_question", methods=["POST"])
def buzz_full_question():
    if request.method == "POST":
        question = request.form.get("text")
    buzzer_string = buzz(question)
    return jsonify({"buzz": buzzer_string})
    
