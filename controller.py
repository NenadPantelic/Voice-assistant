from config.constants import *
from utils.utils import loadJsonData

from services.websearch import wikipedia_search
from exceptions.exception_handler import ExceptionHandler

commands = loadJsonData(ENGLISH_COMMANDS)


servicePool = {

    "wikipedia": wikipedia_search.WikipediaService(language=None)

}

class Controller:
    def __init__(self, recognizer, speaker, commandResolver, executor=None, servicePool={}):
        self.recognizer = recognizer
        self.speaker = speaker
        self.executor = executor
        self.commandResolver = commandResolver
        self.servicePool = servicePool
        self.language = None

    def switchLanguage(self, language):
        assert isinstance(language, str) and language in PROVIDED_LANGUAGES
        self.language = language


    def listenAndSpeakOut(self):
        recognizedSpeech = self.recognizer.recognizeFromMicrophone()
        return self.getOutputSpeech(recognizedSpeech)

    def getOutputSpeech(self, recognizedSpeech):
        recognitionResult = recognizedSpeech.getResult()
        outputMessage = "" if recognitionResult is None else recognitionResult
        messagePrefix = ExceptionHandler.checkExceptionExistence(recognizedSpeech.getStatus(), self.language)
        return messagePrefix + outputMessage

    #this method should be called only once per voice control request
    def determineCommand(self, text):
        command = self.commandResolver.getCommand(text)
        service = self.servicePool[command["service"]]
        executor = getattr(service, command["method"])

        commandResult = executor(command["arg"])









