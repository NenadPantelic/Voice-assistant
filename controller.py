from config.constants import *
from utils.utils import loadJsonData, getCurrentTimestamp

from services.websearch import wikipedia_search
from exceptions.exception_handler import ExceptionHandler

commands = loadJsonData(ENGLISH_COMMANDS)


servicePool = {

    "wikipedia": wikipedia_search.WikipediaService(language=None)

}
#TODO: add json structure checking
#TODO:check if this can be refactored
# languageStr is actuall string that contatins language name
def getLanguageCode(languageStr):
    if "english" in languageStr or "default" in languageStr:
        langChoice = "en"  # "en-US"
    elif "serbian" in languageStr:
        langChoice = "sr"
    else:
        langChoice = None
    return langChoice

class Controller:
    def __init__(self, recognizer, speaker, commandResolver, servicePool={}):
        self.recognizer = recognizer
        self.speaker = speaker
        self.commandResolver = commandResolver
        self.servicePool = servicePool
        self.language = "en"

    def setLanguage(self, languageStr):
        assert isinstance(languageStr, str)
        langCode = getLanguageCode(languageStr)
        self.language = langCode
        self.recognizer.setLanguage(langCode)
        self.speaker.setLanguage(langCode)
        for service in servicePool.values():
            service.setLanguage(langCode)


    def initialize(self):
        self.speaker.speakWithFileSave(self.execute(None))

    def listen(self, init = False):
        return self.recognizer.recognizeFromMicrophone()

    def getCommandOutputText(self, commandResult):
        #TODO:add check if outputMessage and exceptionMessage are nonempty
        exceptionMessage = None
        outputMessage = ""
        if (commandResult is not None):
            outputMessage = "" if commandResult.getResult() is None else commandResult.getResult()
            exceptionMessage = ExceptionHandler.checkExceptionExistence(commandResult.getStatus(), self.language)
        return (outputMessage, exceptionMessage)


    def getOutputSpeech(self, commandResult, message):
        outputMessage, exceptionMessage = self.getCommandOutputText(commandResult)
        messagePrefix = message if exceptionMessage is None else exceptionMessage
        return messagePrefix + outputMessage



    #this method should be called only once per voice control request
    def execute(self, text):
        command = self.commandResolver.getCommand(text)
        commandResult = None
        service = self.servicePool.get(command["service"], None)
        method = command["method"]
        #service is none for setup commands
        if(service is None):
            #NOTE:if method is None - initial speaking, else language setting
            #executor = None
            service = self
            #if(method is None):
                #TODO: map language name to language code - check
        if(method is not None):
            executor = getattr(service, method)
            if(command["hasArgs"]):
                commandResult = executor(command["arg"])
            else:
                commandResult = executor()
        else:
            commandResult = None
        message = command["messages"][self.language]
        return self.getOutputSpeech(commandResult, message)


    def listenAndExecute(self, init=False):
        textResult = self.recognizer.recognizeFromMicrophone()
        output = None
        #tts exception
        if(textResult is None or textResult.getResult() is  None):
            output = self.getOutputSpeech(textResult, '')
        else:
            output = self.execute(textResult.getResult())
        self.speaker.speakWithFileSave(output)






