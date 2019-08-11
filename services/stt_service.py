import speech_recognition as sr

# from config.constants import *
# recognizer = sr.Recognizer()
# from utils.utils import *
'''
recognize_bing(): Microsoft Bing Speech
recognize_google(): Google Web Speech API
recognize_google_cloud(): Google Cloud Speech - requires installation of the google-cloud-speech package
recognize_houndify(): Houndify by SoundHound
recognize_ibm(): IBM Speech to Text
recognize_sphinx(): CMU Sphinx - requires installing PocketSphinx
recognize_wit(): Wit.ai


'''

'''
mic = sr.Microphone()

with mic as source:
    recognizer.adjust_for_ambient_noise(source)
    audio = recognizer.listen(source)
print(recognizer.recognize_google_cloud(audio))
'''

RECOGNITION_METHODS = {

    "bing": "recognize_bing",
    "google": "recognize_google",
    "google_cloud": "recognize_google_cloud",
    "houndify": "recognize_houndify",
    "ibm": "recognize_ibm",
    "sphinx": "recognize_sphinx",
    "wit": "recognize_wit",
    "azure": "recognize_azure"

}


def loggingException(exception):
    print(exception)
    print("Exception message: {}".format(exception))


class SpeechRecognizer:

    def __init__(self, recognitionApi="google", language="en-us", deviceIndex=0):
        self._recognizer = sr.Recognizer()
        self._recognizer.energy_threshold = 500  # type: float
        #below energy_threshold is considered silence, above speech
        self._recognitionApi = recognitionApi
        # self._microphone = None
        self.recognitionMethod = None
        self.determinRecognitionMethod()
        self._microphone = sr.Microphone(deviceIndex)
        self.__language = language


    def setLanguage(self, language):
        self.__language = language

    def getLanguage(self):
        return self.__language

    def determinRecognitionMethod(self):
        apiMethod = RECOGNITION_METHODS.get(self._recognitionApi, "recognize_google()")
        if (self._recognizer is not None and hasattr(self._recognizer, apiMethod)):
            self.recognitionMethod = getattr(self._recognizer, apiMethod)

    def recognizeFromFile(self, audioFile):
        pass

    def recognizeFromMicrophone(self):
        audio = self.getAudioFromMicrophone()
        result = None
        try:
            result = self.recognitionMethod(audio, language=self.__language)
            '''
            if(result is None):
                raise sr.UnknownValueError
            '''
        except sr.UnknownValueError as ex:
            loggingException(ex)
            result = "Speech cannot be analyzed and/or recognized!"

        except sr.RequestError as ex:
            loggingException(ex)
            result = "Request error problem. Check API limits and connectivity status!"

        finally:
            print(result)
            return result

    def getAudioFromMicrophone(self):
        audio = None
        if (self._microphone is not None):
            with self._microphone as source:
                print("Ready for command...")
                self._recognizer.adjust_for_ambient_noise(source)
                audio = self._recognizer.listen(source)
        return audio

'''
srec = SpeechRecognizer(language="sr-RS")
print(srec.recognizeFromMicrophone())
'''
