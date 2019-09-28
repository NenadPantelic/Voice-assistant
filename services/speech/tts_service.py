from config.constants import *
from gtts import gTTS, gTTSError
from playsound import playsound

from services.common.action_result import ActionResult
from utils.utils import get_current_timestamp


class Speaker:
    def __init__(self, lang="en-us"):
        self.__language = lang
        self.tts = gTTS(lang=self.__language, text="dummy")

    def set_language(self, language):
        self.__language = language
        self.tts.lang = self.__language

    def get_language(self):
        return self.__language

    def speak(self, text, fileName=DEFAULT_AUDIO_FILE):
        if fileName != DEFAULT_AUDIO_FILE:
            fileName = PATH_TO_AUDIO_DIR + fileName
        self.tts.text = text
        try:
            self.tts.save(fileName)
            self.play_audio(fileName)
        except gTTSError as e:
            return ActionResult(e, TEXT_TO_SPEECH_EXCEPTION)


    def save_speech_and_play(self, text=''):
        if text != '':
            self.speak(text, str(get_current_timestamp()) + ".mp3")


    def play_audio(self, fileName):
        playsound(fileName)
        # os.remove(fileName)
