from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity 
import nltk
from nltk.corpus import stopwords
import json
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
import re

from nltk.stem.porter import PorterStemmer
import en_core_web_sm

nlp = en_core_web_sm.load()

stopWords = stopwords.words('english')

f = open('app/qanta.json')
data = json.load(f)['data']


questions = []

for i in range(0, len(data)):
    questions.append(data[i]['text'])

f_pop = open('app/query.json')
wiki_population = json.load(f_pop)


countries = list(map(lambda x: x['countryLabel'].lower() , wiki_population))
population = list(map(lambda x: int(x['population']) , wiki_population))

import pycountry

def country_present(question):
    message = ''    
    f_country = open('app/country.json')
    map_instance = json.load(f_country)
    total_instance = sum(map_instance.values())
    print(total_instance)
    for country in map_instance.keys():
        if country in question:
            if len(list(filter(lambda x: x['countryLabel'].lower() == country.lower(), wiki_population))) !=0:
        #     if map_instance[country.name.lower()]/corpus_instance.sum()) < list(filter(lambda x: x['type'] == 1, wiki_population))[0]/population.sum()
                if map_instance[country.lower()]/total_instance < int(list(filter(lambda x: x['countryLabel'].lower() == country.lower(), wiki_population))[0]['population'])/sum(population):
                    message = message + 'The country ' + country + ' in the question is from underrepresented group. The author will get 10 extra points \n'
                else:
                    message = message + 'The country ' + country + ' in the question is from overrepresented group. The author can next time write question having underrepresented countries to earn extra points. \n'
    print(message)
    return message
# tfidf_vectorizer = TfidfVectorizer(stop_words = stopWords)
# tfidf_matrix = tfidf_vectorizer.fit_transform(questions)
# cosine = cosine_similarity(tfidf_matrix[len(questions)-1], tfidf_matrix)[0]
# max_cosine = max(cosine[:len(questions)-1])
# print(max_cosine)

# max_index = np.where(cosine == max_cosine)
# print(questions[max_index[0][0]])

