import speech_recognition as sr
import logging
from config.constants import *
from utils.utils import *
from ..action_result import ActionResult



class SpeechRecognizer:

    def __init__(self, recognition_api="google", language="en-us"):
        self.__recognizer = sr.Recognizer()
        self.__recognizer.energy_threshold = 500  # type: float
        # below energy_threshold is considered silence, above speech
        self.__recognition_api = recognition_api
        self.__recognition_method = None
        self.determine_recognition_method()
        self.__microphone = sr.Microphone()
        self.__language = language

    def set_language(self, language):
        self.__language = language

    def get_language(self):
        return self.__language

    def determine_recognition_method(self):
        apiMethod = RECOGNITION_METHODS.get(self.__recognition_api, "recognize_google")
        if (self.__recognizer is not None and hasattr(self.__recognizer, apiMethod)):
            self.__recognition_method = getattr(self.__recognizer, apiMethod)

    def recognize_from_file(self, audio_file):
        pass

    def recognize_from_microphone(self):
        audio = self.get_audio_from_microphone()
        result = None
        try:
            speech = self.__recognition_method(audio, language=self.__language)
            result = ActionResult(speech, OK)

        except sr.UnknownValueError as e:
            logging_exception(e)
            result = ActionResult(None, UNKNOWN_SPEECH_VALUE_EXCEPTION)

        except sr.RequestError as e:
            logging_exception(e)
            result = ActionResult(None,
                                       REQUEST_SPEECH_EXCEPTION)

        except Exception as e:
            logging_exception(e)
            result = ActionResult(None, DEFAULT_EXCEPTION)

        finally:
            logging.info(result)
            return result

    def get_audio_from_microphone(self):
        audio = None
        if self.__microphone is not None:
            with self.__microphone as source:
                print('Ready for command...')
                logging.info("Ready for command...")
                self.__recognizer.adjust_for_ambient_noise(source)
                audio = self.__recognizer.listen(source)
        return audio

