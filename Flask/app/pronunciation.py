from flask import Flask
from flask import Blueprint, render_template, redirect
from flask import Flask, jsonify, request
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play



pronunciation = Blueprint('pronunciation', __name__)

@pronunciation.route('/getpronunciation', methods=["POST"])
def getpronunciation():
    if request.method == "POST":
        question = request.form.get("text")

    language = 'en'
    myobj = gTTS(text=question, lang=language, slow=False)

    myobj.save("pronunciation.mp3")
    song = AudioSegment.from_mp3("pronunciation.mp3")

    return(song)







