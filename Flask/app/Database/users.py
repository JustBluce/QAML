from flask import Flask, jsonify, request #Flask imports
from flask import Blueprint, render_template, redirect #Flask import to re-route requests on server
from app import db
import json

users = Blueprint('users', __name__)

@users.route("/leaderboard", methods=["GET"])
def leaderboard():
    sql="select Username, points, email from Users ORDER BY points DESC limit 10;"
    result_sql = db.session.execute(sql)
    result_sql = result_sql.fetchall()
    
    result=[]
    for instance in result_sql:
        temp={}
        temp["Name"]=instance[0]
        temp["Score"]=instance[1]
        result.append(temp)

    return jsonify(result)


@users.route("/survey", methods=["POST"])
def survey():
    if request.method == "POST":
        survey = request.form.get("survey")
        

        
    with open('surveys.json', 'w') as outfile:
        json.dump(survey, outfile, indent=2)

    return jsonify("thanks")