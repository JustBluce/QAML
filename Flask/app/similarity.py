from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity 
import nltk
from nltk.corpus import stopwords
import json
import numpy as np
import en_core_web_sm

nlp = en_core_web_sm.load()

stopWords = stopwords.words('english')

f = open('app/qanta.json')
data = json.load(f)['data']


questions = []

for i in range(0, len(data)):
    questions.append(data[i]['text'])

def retrieve_similar_question(new_question):
    questions.append(new_question)
    tfidf_vectorizer = TfidfVectorizer(stop_words = stopWords)
    tfidf_matrix = tfidf_vectorizer.fit_transform(questions)
    cosine = cosine_similarity(tfidf_matrix[len(questions)-1], tfidf_matrix)[0]
    max_cosine = max(cosine[:len(questions)-1])
    print(max_cosine)

    max_index = np.where(cosine == max_cosine)
    print([max_cosine, questions[max_index[0][0]]])
    if max_cosine > 0.7:
        isSimilar = True
    else:
        isSimilar = False
    return [isSimilar, questions[max_index[0][0]]]