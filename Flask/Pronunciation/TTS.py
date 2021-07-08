## DESIGNED by Damian R ##
##Used to create and play audio file#


#gtts is google text to speech so it does require internet
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play

# The text that you want to convert to audio
mytext = 'This is a hard to pronounce sentence.'

# Language in which you want to convert
language = 'en'

# Passing the text and language to the engine,
# here we have marked slow=False. Which tells
# the module that the converted audio should
# have a high speed
myobj = gTTS(text=mytext, lang=language, slow=False)

# Saving the converted audio in a mp3 file named
# welcome
myobj.save("pronunciation.mp3")

file = "pronunciation.mp3"


# Playing the converted file
song = AudioSegment.from_mp3("pronunciation.mp3")
print("Playing pronuncation!")
play(song)




