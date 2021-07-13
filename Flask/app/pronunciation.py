from flask import Flask
from flask import Blueprint, render_template, redirect
from flask import Flask, jsonify, request
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import sys
import speech_recognition as sr
from difflib import SequenceMatcher
import json
from os.path import join, dirname
from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
sys.path.append("..")
sys.path.insert(0, './app')
from app import util, importance
from util import *

authenticator = IAMAuthenticator('Xqq84EWoiOAtKLuKcsA9OUtsekbXDBCgS7FLi2EnNV7i')
speech_to_text = SpeechToTextV1(
    authenticator=authenticator
)

speech_to_text.set_service_url('https://api.us-east.speech-to-text.watson.cloud.ibm.com/instances/21d86f7c-04ec-4029-bef1-abb1ba6586cb')

class MyRecognizeCallback(RecognizeCallback):
    def __init__(self):
        RecognizeCallback.__init__(self)

    def on_data(self, data):
        print(json.dumps(data, indent=2))

    def on_error(self, error):
        print('Error received: {}'.format(error))

    def on_inactivity_timeout(self, error):
        print('Inactivity timeout: {}'.format(error))
    

##compare new and old and return score
def checktexts():
    question_text = open("question.txt").read()
    speech_text = open("speech-text.txt").read()
    m = SequenceMatcher(None, question_text, speech_text)
    decimal = m.ratio()
    percentage = decimal * 100
    as_string = str(percentage)
    print("RATIO OF DIFFERENCE: %s" % as_string)
    return percentage

def Sort(sub_li):
  
    # reverse = None (Sorts in Ascending order)
    # key is set to sort using second element of 
    # sublist lambda has been used
    return(sorted(sub_li, key = lambda x: x[1], reverse = True))  

pronunciation = Blueprint('pronunciation', __name__)
myRecognizeCallback = MyRecognizeCallback()

r = sr.Recognizer()
#question = request.form.get("text")
vectorizer, Matrix, ans = params[0], params[1], params[2]

@pronunciation.route('/get_pronunciation', methods=["POST"])
def getpronunciation():
    if request.method == "POST":
        question = request.form.get("text")


    #question="Hello my name is Damian"
    language = 'en'
    myobj = gTTS(text=question, lang=language, slow=False)
    myobj.save("app/pronunciation.mp3")
    
    question_file = open("app/question.txt","w")
    question_file.write(str(question))
    question_file.close()
    #song = AudioSegment.from_mp3("pronunciation.mp3")
    
    #myRecognizeCallback = MyRecognizeCallback()

    ##audio_file = "app/pronunciation.mp3"

    with open(join(dirname(__file__), './.', "pronunciation.mp3"),'rb') as audio_file:
        speech_recognition_results = speech_to_text.recognize(
            audio=audio_file,
            content_type='audio/mp3',
            word_alternatives_threshold=0.9,
            word_confidence = True
        ).get_result()
    
    transcribed_text = speech_recognition_results["results"][0]["alternatives"][0]["transcript"]
    confidence = speech_recognition_results["results"][0]["alternatives"][0]["confidence"]
    array_of_word_confidence = []
    for i in speech_recognition_results["results"][0]["alternatives"][0]["word_confidence"]:
        array_of_word_confidence.append([i[0],i[1]])

    repre = vectorizer.transform([question])
    repre_transcribed = vectorizer.transform([transcribed_text])
    print(repre)
    matrix = repre.dot(repre_transcribed.T).T
    cosine_similarity = matrix.toarray()[0][0]
    most_difficult_to_pronounce_words = Sort(array_of_word_confidence)[0:3]
    answer = []
    for i in most_difficult_to_pronounce_words:
        answer.append({"Word": i[0], "Score":i[1]})

    # file = open("app/speech-text.txt","w")
    # file.write(json.dumps(speech_recognition_results, indent=2))
    # file.close()

    if(cosine_similarity < threshold):
        return answer


    
    return None

   




# with open(join(dirname(__file__), './.', audio_file),'rb') as audio_file:
#    audio_source = AudioSource(audio_file)
 #   speech_to_text.recognize_using_websocket(
  #      audio=audio_source,
   #     content_type='audio/mp3',
    #    recognize_callback=myRecognizeCallback,
     #   model='en-US_BroadbandModel',)



    ##return("hello world")




