from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity 
import nltk
from nltk.corpus import stopwords
import json
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
import re
from flask import Blueprint, render_template, redirect
from flask import Flask, jsonify, request
from nltk.stem.porter import PorterStemmer
import en_core_web_sm
import time
import sys
sys.path.append("..")
sys.path.insert(0, 'C:/Users/Rahi/Downloads/TryoutProject-main/TryoutProject-main/Flask/app')

stopWords = stopwords.words('english')

f = open('app/qanta.json')
data = json.load(f)['questions']


questions = []

for i in range(0, len(data)):
    questions.append(data[i]['text'])

f_pop = open('app/query.json')
wiki_population = json.load(f_pop)


countries = list(map(lambda x: x['countryLabel'].lower() , wiki_population))
population = list(map(lambda x: int(x['population']) , wiki_population))

import pycountry
country_represent = Blueprint('country_represent', __name__)
@country_represent.route("/country_present", methods=["POST"])

def country_present():
    if request.method == "POST":
        question = request.form.get("text")
    start = time.time()
    message = ''    
    f_country = open('app/country.json')
    map_instance = json.load(f_country)
    total_instance = sum(map_instance.values())
    print(total_instance)
    under_countries = []
    over_countries = []
    for country in map_instance.keys():
        if country in question.lower():
            if len(list(filter(lambda x: x['countryLabel'].lower() == country.lower(), wiki_population))) !=0:
                if map_instance[country.lower()]/total_instance < int(list(filter(lambda x: x['countryLabel'].lower() == country.lower(), wiki_population))[0]['population'])/sum(population):
                    under_countries.append(country)
                else:
                    over_countries.append(country) 
    if len(under_countries) != 0: 
        message = message + 'The country ' + ', '.join(under_countries) + ' in the question is/are from underrepresented group. The author will get 10 extra points \n'
    else:
         message = message + 'The country ' + ', '.join(over_countries) + ' in the question is/are from overrepresented group. The author can next time write question having underrepresented countries to earn extra points. \n'
    print(message)
    end = time.time()
    print(end - start)
    return jsonify({"country_representation" : message})

