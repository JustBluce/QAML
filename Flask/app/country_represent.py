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
from scipy.spatial.distance import cosine
import en_core_web_sm
import time
import sys
import torch
sys.path.append("..")
sys.path.insert(0, './app')

nlp = en_core_web_sm.load()

stopWords = stopwords.words('english')

f = open('app/qanta.json')
data = json.load(f)['questions']
import re
# import gensim.downloader as api
# pre_ft_vectors = api.load('fasttext-wiki-news-subwords-300')


from transformers import AutoTokenizer,AutoModelForSequenceClassification, AutoModelForPreTraining
tokenizer = AutoTokenizer.from_pretrained('albert-base-v2', do_lower_case=True)
model = AutoModelForPreTraining.from_pretrained("albert-base-v2", output_attentions=False, output_hidden_states=True)

def break_into_words_with_capital(question):
    array_of_words =re.split('(?=[A-Z]| )', question)

    return list(filter(None, [x.strip() for x in array_of_words])) 

# def vectorizer(string):
#   vectors = []
#   string_vec = np.zeros(300)
#   array_of_words = break_into_words_with_capital(string)
#   # print(array_of_words)
#   for i in range(len(array_of_words)):
#     if array_of_words[i] in pre_ft_vectors:
      
#       vec = pre_ft_vectors[array_of_words[i]]
#       string_vec = string_vec + vec
#     else:
#       vec = np.zeros(300)
#     vectors.append(vec)
#   string_vec = string_vec/len(array_of_words)
#   return string_vec

def bert_text_preparation(text, tokenizer):
    """Preparing the input for BERT

    Takes a string argument and performs
    pre-processing like adding special tokens,
    tokenization, tokens to ids, and tokens to
    segment ids. All tokens are mapped to seg-
    ment id = 1.

    Args:
        text (str): Text to be converted
        tokenizer (obj): Tokenizer object
            to convert text into BERT-re-
            adable tokens and ids

    Returns:
        list: List of BERT-readable tokens
        obj: Torch tensor with token ids
        obj: Torch tensor segment ids


    """
    marked_text = "[CLS] " + text + " [SEP]"
    tokenized_text = tokenizer.tokenize(marked_text)
    indexed_tokens = tokenizer.convert_tokens_to_ids(tokenized_text)
    segments_ids = [1]*len(indexed_tokens)

    # Convert inputs to PyTorch tensors
    tokens_tensor = torch.tensor([indexed_tokens])
    segments_tensors = torch.tensor([segments_ids])

    return tokenized_text, tokens_tensor, segments_tensors

def get_bert_embeddings(tokens_tensor, segments_tensors, model):
    """Get embeddings from an embedding model

    Args:
        tokens_tensor (obj): Torch tensor size [n_tokens]
            with token ids for each token in text
        segments_tensors (obj): Torch tensor size [n_tokens]
            with segment ids for each token in text
        model (obj): Embedding model to generate embeddings
            from token and segment ids

    Returns:
        list: List of list of floats of size
            [n_tokens, n_embedding_dimensions]
            containing embeddings for each token

    """
    
    # Gradient calculation id disabled
    # Model is in inference mode
    with torch.no_grad():
        outputs = model(tokens_tensor, segments_tensors)
        # Removing the first hidden state
        # The first state is the input state
        hidden_states = outputs.hidden_states[1:]
#         print(len(outputs))
    # Getting embeddings from the final BERT layer
    token_embeddings = hidden_states[-1]
    # Collapsing the tensor into 1-dimension
    token_embeddings = torch.squeeze(token_embeddings, dim=0)
    # Converting torchtensors to lists
    list_token_embeddings = [token_embed.tolist() for token_embed in token_embeddings]

    return list_token_embeddings

def vectorize_albert(text):
  text = " ".join(break_into_words_with_capital(text))
  
  
  tokenized_text, tokens_tensor, segments_tensors = bert_text_preparation(text, tokenizer)
  list_token_embeddings = get_bert_embeddings(tokens_tensor, segments_tensors, model)
  tweet_embedding = np.mean(np.array(list_token_embeddings), axis=0)
  
  return tweet_embedding
    

questions = []

for i in range(0, len(data)):
    questions.append(data[i]['text'])

f_pop = open('app/query.json')
wiki_population = json.load(f_pop)


countries = list(map(lambda x: x['countryLabel'].lower() , wiki_population))
population = list(map(lambda x: int(x['population']) , wiki_population))

import pycountry
country_represent = Blueprint('country_represent', __name__)
f_country = open('app/country.json')
map_instance = json.load(f_country)
total_instance = sum(map_instance.values())

def Sort(sub_li):
  
    # reverse = None (Sorts in Ascending order)
    # key is set to sort using second element of 
    # sublist lambda has been used
    return(sorted(sub_li, key = lambda x: x[1], reverse = True))



@country_represent.route("/country_present", methods=["POST"])
def country_present():
    if request.method == "POST":
        question = request.form.get("text")
    start = time.time()
    message = ''    
    # print(vectorizer("british"))
    # print(total_instance)
    under_countries = []
    over_countries = []
    for country in map_instance.keys():
        # if country in question.lower():
        if len(list(filter(lambda x: x['countryLabel'].lower() == country.lower(), wiki_population))) !=0:
            if map_instance[country.lower()]/total_instance < int(list(filter(lambda x: x['countryLabel'].lower() == country.lower(), wiki_population))[0]['population'])/sum(population): 
                under_countries.append(country)
            else:
                over_countries.append(country) 
    # print(under_countries)
    question_vector = vectorize_albert(question)
    cosine_sim_ques_country = []
    for i in under_countries:
        # b = " ".join(x for x in i)
        cosine_sim_ques_country.append([ i, 1 - cosine(question_vector, vectorize_albert(i)) ])
    # if len(under_countries) != 0: 
    #     message = message + 'The country ' + ', '.join(under_countries) + ' in the question is/are from underrepresented group. The author will get 10 extra points. \n'
    # else:
    #      message = message + 'The country ' + ', '.join(over_countries) + ' in the question is/are from overrepresented group. The author can next time write question having underrepresented countries to earn extra points. \n'
    message = Sort(cosine_sim_ques_country)
    end = time.time()
    print("----TIME (s): /country_represent/country_present---",end - start)
    return jsonify({"country_representation" : message})