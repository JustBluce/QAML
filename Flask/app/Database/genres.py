from flask import Flask, jsonify, request #Flask imports
from flask import Blueprint, render_template, redirect #Flask import to re-route requests on server
from app import db

genres = Blueprint('genres', __name__)

@genres.route("/getGenre", methods=["GET"])
def getGenre(uid):
    sql="select count(*) from Question Where Genre='History' and UserId=%s" %uid
    ##sql="select username, points from Users ORDER BY points DESC limit 10;"
    result_sql = db.session.execute(sql)
    result_sql = result_sql.fetchall()
    
    result=[]
    for instance in result_sql:
        temp={}
        temp["Genre"]="History"
        #temp["Genre"]=instance[0]
        temp["Count"]=instance[0]
        result.append(temp)

    return jsonify(result)

    