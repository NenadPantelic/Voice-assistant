import speech_recognition as sr
import logging
from config.constants import *
from utils.utils import *



class SpeechRecognizer:

    def __init__(self, recognitionApi="google", language="en-us"):
        self.__recognizer = sr.Recognizer()
        self.__recognizer.energy_threshold = 500  # type: float
        # below energy_threshold is considered silence, above speech
        self.__recognitionApi = recognitionApi
        self.__recognitionMethod = None
        self.determinRecognitionMethod()
        self.__microphone = sr.Microphone()
        self.__language = language

    def setLanguage(self, language):
        self.__language = language

    def getLanguage(self):
        return self.__language

    def determinRecognitionMethod(self):
        apiMethod = RECOGNITION_METHODS.get(self.__recognitionApi, "recognize_google")
        if (self.__recognizer is not None and hasattr(self.__recognizer, apiMethod)):
            self.__recognitionMethod = getattr(self.__recognizer, apiMethod)

    def recognizeFromFile(self, audioFile):
        pass

    def recognizeFromMicrophone(self):
        audio = self.getAudioFromMicrophone()
        result = None
        try:
            speech = self.__recognitionMethod(audio, language=self.__language)
            result = RecognitionResult(speech, OK)
            '''
            if(result is None):
                raise sr.UnknownValueError
            '''
        except sr.UnknownValueError as e:
            loggingException(e)
            result = RecognitionResult("Speech cannot be analyzed and/or recognized!", UNKNOWN_SPEECH_VALUE_EXCEPTION)

        except sr.RequestError as e:
            loggingException(e)
            result = RecognitionResult("Request error problem. Check API limits and connectivity status!",
                                       REQUEST_SPEECH_EXCEPTION)

        except Exception as e:
            loggingException(e)
            result = RecognitionResult(e, DEFAULT_EXCEPTION)

        finally:
            logging.info(result)
            return result

    def getAudioFromMicrophone(self):
        audio = None
        if (self.__microphone is not None):
            with self.__microphone as source:
                print('Ready for command...')
                logging.info("Ready for command...")
                self.__recognizer.adjust_for_ambient_noise(source)
                audio = self.__recognizer.listen(source)
        return audio



class RecognitionResult:
    def __init__(self, result, status):
        self.__result = result
        self.__status = status

    # getters
    def getResult(self):
        return self.__result

    def getStatus(self):
        return self.__status

    def setResult(self, result):
        self.__result = result

    def setStatus(self, status):
        self.__status = status
