# Raj

# Description of this file: This is the a file that contains all the import statements.

import re #Regex library
import warnings #Operating system warnings
warnings.filterwarnings("ignore")
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import sys #Importing the system
sys.path.append("..")
sys.path.insert(0, './app') #Adding the path to the files on the system
from app import db, metadata #Import access to the metadata and database
from flask import Flask, jsonify, request #Flask imports
from flask import Blueprint, render_template, redirect #Flask import to re-route requests on server
import transformers #For the huggingface models
import sklearn #Importing the scikit learn library
from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoModelForPreTraining, AutoConfig #Functions to help import the pretrained models
import pycountry #Get details about countries
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer #To train a new tf-idf vectorizer on the qanta question database
from sklearn.metrics.pairwise import cosine_similarity #To calculate cosine similarity
import nltk 
import spacy
from nltk.corpus import stopwords
import json
import numpy as np
from nltk.stem.porter import PorterStemmer
from scipy.spatial.distance import cosine
import en_core_web_sm
import time
import torch
import wikipedia
import tensorflow as tf
from transformers import BertTokenizer, BertForSequenceClassification, RobertaForSequenceClassification, RobertaTokenizer, DistilBertForSequenceClassification, DistilBertTokenizer
from tabulate import tabulate
from collections import defaultdict
from typing import List, Optional, TYPE_CHECKING, Tuple
import decimal
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from ethnicolr import census_ln, pred_census_ln, pred_wiki_ln
import pandas as pd
import requests
from spacy import displacy
from collections import Counter
import pickle
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import speech_recognition as sr
from difflib import SequenceMatcher
from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
# nltk.download('punkt') #Download once
from transformers import logging
logging.set_verbosity_error()
from datetime import datetime
import functools
import fuzzywuzzy
from fuzzywuzzy import fuzz
import itertools
import string