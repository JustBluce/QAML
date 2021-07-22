from flask import Flask, jsonify, request
from util import *
from app import util
from flask import Blueprint, render_template, redirect
import sys
import re
from importance import *
sys.path.append("..")
sys.path.insert(0, './app')

over_present = Blueprint('over_present', __name__)


@over_present.route("highlight", methods=["POST"])
def high_light():
    if request.method == "POST":
        question = request.form.get("text")
        answer = request.form.get("answer_text")
    
    temp_var = guess_top_n(question=[question], params=params, n=1)[0][0]
    if answer != temp_var:
        return []

    highlight = []
    array_of_important_word_to_delay_buzzer, array_of_important_word_to_right_answer = get_important_word_to_delay_the_buzzer(question, answer)
    array_of_important_sentence_to_right_answer = get_important_sentence_to_get_right_answer(question, answer)


    highlight.extend(highlight_json(items=array_of_important_word_to_right_answer, color="#e91640"))
    highlight.extend(highlight_json(items=array_of_important_sentence_to_right_answer, color="#e91640"))
    highlight.extend(highlight_json(items=array_of_important_word_to_delay_buzzer, color="#fff05e"))

    return jsonify({"highlight": highlight})
