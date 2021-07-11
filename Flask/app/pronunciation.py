from flask import Flask
from flask import Blueprint, render_template, redirect
from flask import Flask, jsonify, request
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import sys
import speech_recognition as sr
from difflib import SequenceMatcher
sys.path.append("..")
sys.path.insert(0, './app')



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


    

pronunciation = Blueprint('pronunciation', __name__)

r = sr.Recognizer()
#question = request.form.get("text")


@pronunciation.route('/getpronunciation', methods=["POST"])
def getpronunciation():
    if request.method == "POST":
        question = request.form.get("text")

    language = 'en'
    myobj = gTTS(text=question, lang=language, slow=False)
    myobj.save("pronunciation.mp3")
    question_file = open("question.txt","w")
    question_file.write(question)
    question_file.close()
    #song = AudioSegment.from_mp3("pronunciation.mp3")

    transcription = sr.AudioFile('pronunciation.mp3')
    with transcription as source:
        audio = r.record(source)
    
    ## DEBUGGING
    print(r.recognize_sphinx(audio))

    file = open("speech-text.txt","w")
    file.write(r.recognize_sphinx(audio))
    file.close()

    checktexts()

    ##return("hello world")




