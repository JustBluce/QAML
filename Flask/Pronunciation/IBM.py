import json
from os.path import join, dirname
from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

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
    
   

myRecognizeCallback = MyRecognizeCallback()

audio_file = "pronunciation.mp3"


# with open(join(dirname(__file__), './.', audio_file),'rb') as audio_file:
#    audio_source = AudioSource(audio_file)
 #   speech_to_text.recognize_using_websocket(
  #      audio=audio_source,
   #     content_type='audio/mp3',
    #    recognize_callback=myRecognizeCallback,
     #   model='en-US_BroadbandModel',)

with open(join(dirname(__file__), './.', audio_file),'rb') as audio_file:
    speech_recognition_results = speech_to_text.recognize(
        audio=audio_file,
        content_type='audio/mp3',
        word_alternatives_threshold=0.9,
    ).get_result()

print(json.dumps(speech_recognition_results, indent=2))





