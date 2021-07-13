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
    return(sorted(sub_li, key = lambda x: x[2], reverse = False))   

pronunciation = Blueprint('pronunciation', __name__)
myRecognizeCallback = MyRecognizeCallback()

r = sr.Recognizer()
#question = request.form.get("text")
vectorizer, Matrix, ans = params[0], params[1], params[2]

@pronunciation.route('/get_pronunciation', methods=["POST"])
def getpronunciation():
    if request.method == "POST":
        question = request.form.get("text")

    start = time.time()
    if(not(question)):
        jsonify({"pronunciation": [{"Word": "-", "Score":"-"}]})

    question = " " + question
    language = 'en'
    myobj = gTTS(text=question, lang=language, slow=False)
    myobj.save("app/pronunciation.mp3")
    
    # question_file = open("app/question.txt","w")
    # question_file.write(str(question))
    # question_file.close()
    

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
    # print(repre)
    matrix = repre.dot(repre_transcribed.T).T
    cosine_similarity = matrix.toarray()[0][0]
    temp_word_array = break_into_words(question)
    print(temp_word_array)
    print(array_of_word_confidence)
    count = 0
    array = []
    while("" in temp_word_array) :
        temp_word_array.remove("")
    for i in range(len(array_of_word_confidence)):
        array.append([temp_word_array[i], array_of_word_confidence[i][0], array_of_word_confidence[i][1]])
    most_difficult_to_pronounce_words = Sort(array)[:3]
    answer = []
    for i in range(len(most_difficult_to_pronounce_words)):
        answer.append({"Original_Word": most_difficult_to_pronounce_words[i][0], "Transcribed_Word": most_difficult_to_pronounce_words[i][1], "Score":most_difficult_to_pronounce_words[i][2]})
    # file = open("app/speech-text.txt","w")
    # file.write(json.dumps(speech_recognition_results, indent=2))
    # file.close()
    end = time.time()
    print("----TIME (s) : /pronunciation/get_pronunciation---", end - start)
    if(cosine_similarity < threshold_pronunciation):
        return jsonify({"pronunciation": answer})
    

    
    return jsonify({"pronunciation": [{"Word": "-", "Score":"-"}]})

   




# with open(join(dirname(__file__), './.', audio_file),'rb') as audio_file:
#    audio_source = AudioSource(audio_file)
 #   speech_to_text.recognize_using_websocket(
  #      audio=audio_source,
   #     content_type='audio/mp3',
    #    recognize_callback=myRecognizeCallback,
     #   model='en-US_BroadbandModel',)



    ##return("hello world")




