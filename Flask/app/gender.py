import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm

nlp = en_core_web_sm.load()
import requests
from flask import jsonify, make_response
import json
import pandas as pd
from ethnicolr import census_ln, pred_census_ln, pred_wiki_ln
from app.ethnic import find_ethnicity
spacy.load('en_core_web_sm')

def getGender(text):

    doc = nlp(text)
    entities = [(X.text, X.label_) for X in doc.ents]
    names = []
    
    for i in range(0, len(entities)):
        if(entities[i][1] == 'PERSON'):
            resp = requests.get('https://gender-api.com/get?name='+ entities[i][0] +'&key=8ntwZAbqzWJEsldFDVfk8jxLlZCgU9WYEK4Y')
            names.append(resp.json()['name'] + '(' + resp.json()['gender'] + ', ' + find_ethnicity(resp.json()['name'])+' )')
            print(resp.json())
            
    return names