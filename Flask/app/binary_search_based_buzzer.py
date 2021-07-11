# Raj
import warnings
from importance import *
from util import *
from app import util, importance
import sys
from app import db, metadata
from flask import Flask, jsonify, request
from flask import Blueprint, render_template, redirect


def warn(*args, **kwargs):
    pass


warnings.warn = warn
sys.path.append("..")
sys.path.insert(0, './app')


binary_search_based_buzzer = Blueprint('binary_search_based_buzzer', __name__)


def buzz(question, min_index=5):

    answer = []
    # temp_word_array = break_into_words(question)
    temp_word_array = question.split(' ')
    # check if buzzer ever goes above threshold
    index_of_bin_search = len(temp_word_array)
    question_sentence = question
    temp_var = guess_top_n(
        question=[question_sentence], params=params, max=3, n=1)
    if(temp_var[0][1] < threshold):
        return "Buzzer never crosses the threshold", False
    store_index = index_of_bin_search
    max_index = index_of_bin_search - 1

    while max_index >= min_index:
        index_of_bin_search = (max_index+min_index)//2
        question_sentence = " ".join(temp_word_array[:index_of_bin_search])
        temp_var = guess_top_n(
            question=[question_sentence], params=params, max=3, n=1)
        if (temp_var[0][1] > threshold):
            max_index = index_of_bin_search-1
            store_index = index_of_bin_search
        else:
            min_index = index_of_bin_search+1
    # print("Index is :" + str(store_index) + " and the score is " + str(temp_var[0][1]) + " with guess = " + str(temp_var[0][0]) )

    return question_sentence, True


@binary_search_based_buzzer.route("/buzz_full_question", methods=["POST"])
def buzz_full_question():
    if request.method == "POST":
        question = request.form.get("text")
    start = time.time()
    buzzer_string, flag = buzz(question)
    end = time.time()
    # print(end - start)
    print("----TIME (s) : /binary_search_based_buzzer/buzz_full_question---", end - start)

    start = time.time()
    if(flag):
        importance_sentence = get_importance_of_each_sentence(buzzer_string)
        buzzer_string = buzzer_string + " ||BUZZ||"
    else:
        print("question")
        print(question)
        importance_sentence = get_importance_of_each_sentence(question)
    end = time.time()
    # print(end - start)
    print("----TIME (s) : /binary_search_based_buzzer/get_importance_sentence---", end - start)
    return jsonify({"buzz": buzzer_string, "importance": importance_sentence})
