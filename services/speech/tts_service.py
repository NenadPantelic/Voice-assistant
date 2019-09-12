from config.constants import *
from gtts import gTTS
from playsound import playsound


class Speaker:
    def __init__(self, lang="en-us"):
        self.__language = lang
        self.tts = gTTS(lang=self.__language, text="dummy")

    def setLanguage(self, language):
        self.__language = language
        self.tts.lang = self.__language

    def getLanguage(self):
        return self.__language

    def speak(self, text, fileName=DEFAULT_AUDIO_FILE):
        if (fileName != DEFAULT_AUDIO_FILE):
            fileName = PATH_TO_AUDIO_DIR + fileName
        self.tts.text = text
        self.tts.save(fileName)
        self.playAudio(fileName)

    def playAudio(self, fileName):
        playsound(fileName)
        # os.remove(fileName)
