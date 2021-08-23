from flask import Blueprint, render_template, request, jsonify
import json
import os
import re
from app import db

test1 = Blueprint('test1', __name__)

# TODO Database operation of table Question

class Question_json(db.Model):
    __tablename__ = 'Question_json'
    q_id = db.Column(db.String, primary_key=True)
    data = db.Column(db.JSON)
    points = db.Column(db.Integer)
    UID = db.Column(db.String)

class Users(db.Model):
    __tablename__ = 'Users'
    q_id = db.Column(db.String, primary_key=True)
    data = db.Column(db.JSON)
    points = db.Column(db.Integer)
    UID = db.Column(db.String)

@test1.route('/json', methods=['POST, GET'])
def test_json():
    if request.method == 'POST':
        pass
    else:
        pass

    with open('./app/Database/test.json', 'r') as load_f:
        load_dict = json.load(load_f)
    q_id = load_dict["q_id"]
    data = load_dict["data"]
    UID = load_dict["UID"]

    # points must have been calculated
    points = 12

    # insert question data
    try:
        me = Question_json(q_id=q_id, data=data, UID=UID, points=points)
        db.session.add(me)
        db.session.commit()
        message_json = "Successfully insert a new question_json record of the edit history of question"
    except:
        message_json = "Error insert a new question_json record of the edit history of question"

    try:
        pass
    else:
        pass

    return message_json