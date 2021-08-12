from flask import Blueprint, render_template, request, jsonify
from app import db

question = Blueprint('question', __name__)

@question.route('/Question_id', methods=['POST'])
def Question_id():
    if request.method == 'POST':
        Timestamp = request.form.get('Timestamp')
    sql1='select max(Question_id) from Question'
    result_sql = db.session.execute(sql1)
    result_sql = result_sql.fetchall()
    Question_id = result_sql[0][0] + 1

    sql2='insert Question (Question_id, Timestamp) VALUE ('+str(Question_id)+', \''+Timestamp+'\')'
    result_sql = db.session.execute(sql2)

    return Question_id

@question.route('/Question', methods=['POST'])
def Question():
    if request.method == 'POST':
        Question=request.form.get('Question')
        Answer=request.form.get('Answer')
    pass