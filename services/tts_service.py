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

PATH_TO_AUDIO_DIR = r"data/audio/"
DEFAULT_AUDIO_FILE = PATH_TO_AUDIO_DIR + "temporary.mp3"

class Speaker:
    def __init__(self, lang = "en-us"):
        self.__language = lang
        self.tts = gTTS(lang = self.__language, text="blahblah")

    def setLanguage(self, language):
        self.__language = language
        self.tts.lang = self.__language

    def getLanguage(self):
        return self.__language

    def speak(self, text, fileName =  DEFAULT_AUDIO_FILE):
        if(fileName != DEFAULT_AUDIO_FILE):
            fileName = PATH_TO_AUDIO_DIR + fileName
        self.tts.text = text
        self.tts.save(fileName)
        self.playAudio(fileName)

    def playAudio(self, fileName):
        playsound(fileName)
        #os.remove(fileName)


