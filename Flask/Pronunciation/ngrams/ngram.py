from flask import Flask, request,jsonify,json
from flask_cors import CORS, cross_origin
import os
import subprocess
import json


app = Flask(__name__)
Cors = CORS(app)
CORS(app, resources={r'/*': {'origins': '*'}},CORS_SUPPORTS_CREDENTIALS = True)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/ngram", methods=["POST","GET"])
def submitData():
  response_object = {'status':'success'}
  if request.method == "POST":
     question = request.form.get("text")
     
     ##subprocess.run(["cd", "/Users/Damian/Documents/GitHub/language-detector-node"])
   ##output = subprocess.run(["npm run detect", "/Users/Damian/Documents/GitHub/language-detector-node"])
     output = os.system("npm run detect '%s' " % question) 
     
     print(question)
     print(output)
     

     response_object['answer'] ='Data added!'
     return jsonify(response_object)


if __name__ == '__main__':    
   app.run(debug=True)