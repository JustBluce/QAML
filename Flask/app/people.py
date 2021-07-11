import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
import time
nlp = en_core_web_sm.load()
import requests
import json
spacy.load('en_core_web_sm')
from flask import Blueprint, render_template, redirect
from flask import Flask, jsonify, request

import pandas as pd
from ethnicolr import census_ln, pred_census_ln, pred_wiki_ln
import sys
sys.path.append("..")
sys.path.insert(0, './app')

def find_ethnicity(name): 
    names = [{'name': name}]
    df = pd.DataFrame(names)

    # print(census_ln(df, 'name'))
    return pred_wiki_ln(df, 'name')['race'][0] 

people_info = Blueprint('people_info', __name__)
@people_info.route("/getPeoplesInfo", methods=["POST"])
def getPeoplesInfo():
    
    if request.method == "POST":
        question = request.form.get("text")
    start = time.time()
    doc = nlp(question)
    entities = [(X.text, X.label_) for X in doc.ents]
    print(entities)
    person=[]
    names = []
    for i in range(0, len(entities)):
        if(entities[i][1] == 'PERSON'):
            person.append(entities[i][0])
            names.append(entities[i][0] + '( ' + find_ethnicity(entities[i][0])+' )')
            print(entities[i][0] + '( ' + find_ethnicity(entities[i][0])+' )')
    end = time.time()
    print("----TIME (s) : /people_info/getPeoplesInfo---", end - start)
    return jsonify({"people_ethnicity" : ' '.join(names), "person": person})