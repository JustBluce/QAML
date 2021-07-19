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
import subprocess
import os 

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
    
 

pronunciation = Blueprint('pronunciation', __name__)
myRecognizeCallback = MyRecognizeCallback()

r = sr.Recognizer()
#question = request.form.get("text")

#for bigger questions only
def shrink_and_split():
    command = "ffmpeg -i /audio_files/pronunciation.mp3 -f segment -segment_time 360 -c copy %03d.mp3"
    subprocess.call(command, shell=True)

    files = []
    path = os.getcwd()
    path = path + "audio_files"

    for filename in os.listdir(path):
        if filename.endswith(".mp3") and filename != 'pronunciation.mp3':
            files.append(filename)
    files.sort()

    ##transcription
    results = []
    for filename in files: 
        with open(filename, 'rb') as f:
            res = speech_to_text.recognize(audio=f, content_type='audio/mp3', model='en-US_NarrowbandModel', continuous=True, inactivity_timeout=360).get_result()
            results.append(res)
    text = []
    for file in results: 
        for result in file['results']:
            text.append(result['alternatives'][0]['transcript'].rstrip() + '.\n')

    speech_file = open(path + "speech-text.txt","w")
    speech_file.write(text)
    speech_file.close()
   



@pronunciation.route('/get_pronunciation', methods=["POST"])
def getpronunciation():
    if request.method == "POST":
        question = request.form.get("text")

    start = time.time()
    question = " " + question
    language = 'en'
    myobj = gTTS(text=question, lang=language, slow=True)
    myobj.save("app/audio_files/pronunciation.mp3")
    
    question_file = open("app/question.txt","w")
    question_file.write(str(question))
    question_file.close()
    

    with open(join(dirname(__file__), './audio_files/', "pronunciation.mp3"),'rb') as audio_file:
        speech_recognition_results = speech_to_text.recognize(
            audio=audio_file,
            content_type='audio/mp3',
            model='en-US_NarrowbandModel',
            continuous=True,
            word_confidence = False
        ).get_result()
    
    transcribed_text = speech_recognition_results["results"][0]["alternatives"][0]["transcript"]
    
    speech_file = open("app/audio_files/speech-text.txt","w")
    speech_file.write(transcribed_text)
    speech_file.close()
   
    end = time.time()
    final_time = end - start
    print("----TIME (%.2f) : /pronunciation/get_pronunciation---" % (final_time))

    print(transcribed_text)
    return jsonify({"message": [transcribed_text]})
       

   


