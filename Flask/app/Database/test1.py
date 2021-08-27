from flask import Blueprint, render_template, request, jsonify
import json
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
    UID = db.Column(db.String, primary_key=True)
    username = db.Column(db.String)
    email = db.Column(db.String)
    points = db.Column(db.Integer)

@test1.route('/json', methods=['POST'])
def test_json():
    if request.method == 'POST':
        UID = request.form.get('UID')
        username = request.form.get('username')
        email = request.form.get('email')

    user = Users.query.filter_by(UID=UID).first()
    if user is None:
        user = Users(username = username, email = email, UID = UID, points = 0)
        db.session.add(user)
        db.session.commit()
        message_user = "create new user"
    else:
        message_user = "user already exists"

    with open('./app/Database/test.json', 'r') as load_f:
        load_dict = json.load(load_f)
    q_id = load_dict["q_id"]
    data = load_dict["data"]

    # points must have been calculated
    points = 12

    # insert question data
    try:
        question = Question_json(q_id=q_id, data=data, UID=UID, points=points)
        db.session.add(question)
        db.session.commit()
        message_json = "Successfully insert a new question_json record of the edit history of question"
    except:
        message_json = "Error insert a new question_json record of the edit history of question"

    try:
        user = Users.query.filter(Users.UID == UID).first()
        user.points = user.points + points
        db.session.commit()
        message_points = "Successfully change the points of the user."
    except:
        message_points = "Error change the points of the user."

    return {"message_user": message_user, "message_json": message_json, "message_points": message_points}