from flask import Flask, jsonify, request #Flask imports
from flask import Blueprint, render_template, redirect #Flask import to re-route requests on server
from app import db
import json
from import_libraries import *
import datetime
sys.path.append("..")
sys.path.insert(0, './app/Database/Surveys')
#os.chdir(os.getcwd()+"/app/Database/Surveys") 


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
        survey = request.json
    
    start = time.time()
    
    #
    basename="survey"
    suffix = datetime.datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
    filename = "_".join([basename, suffix]) 
    filename = str(filename + ".json")
     

    with open(filename , 'w+') as outfile:
        ##outfile.write(survey)
        json.dump(survey, outfile, indent=2)
    
    end = time.time()
    print("----TIME (s) : /users/survey---", end - start)

    return jsonify("thanks")