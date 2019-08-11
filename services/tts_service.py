import pyttsx3
#engine = pyttsx3.init()
#engine.say('Good morning.')
#engine.runAndWait()

import gtts
from gtts import gTTS
import os
#tts = gTTS(text='Jedi govna!', lang='sr')
#print(gtts.lang.tts_langs())
#tts.save("good.mp3")
#os.system("mpg321 good.mp3")
from io import BytesIO
#mp3_fp = BytesIO()
#tts = gTTS('hello', 'en')
#tts.write_to_fp(mp3_fp)

from playsound import playsound
#playsound('good.mp3')


class Speaker:
    def __init__(self, lang = "en-us"):
        self.language = lang
        self.tts = gTTS(lang = self.language, text="blahblah")

    def speak(self, text, fileName = "temporary.mp3"):
        self.tts.text = text
        self.tts.save(fileName)
        self.playAudio(fileName)

    def playAudio(self, fileName):
        playsound(fileName)


