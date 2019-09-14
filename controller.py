from config.constants import *
from utils.utils import loadJsonData, getCurrentTimestamp

from services.websearch import wikipedia_search
from exceptions.exception_handler import ExceptionHandler

commands = loadJsonData(ENGLISH_COMMANDS)


servicePool = {

    "wikipedia": wikipedia_search.WikipediaService(language=None)

}


# languageStr is actuall string that contatins language name
def getLanguageCode(languageStr):
    if "english" in languageStr or "default" in languageStr:
        langChoice = "en-US"  # "en-US"
    elif "serbian" in languageStr:
        langChoice = "sr-RS"
    else:
        langChoice = None
    return langChoice

class Controller:
    def __init__(self, recognizer, speaker, commandResolver, executor=None, servicePool={}):
        self.recognizer = recognizer
        self.speaker = speaker
        self.executor = executor
        self.commandResolver = commandResolver
        self.servicePool = servicePool
        self.language = "en"

    def switchLanguage(self, language):
        assert isinstance(language, str) and language in PROVIDED_LANGUAGES
        self.language = language


    def listen(self, init = False):
        return None if init else self.recognizer.recognizeFromMicrophone()

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
            executor = None
            if(method is not None):
                lang = command["arg"]
                #TODO: map language name to language code
                self.switchLanguage(getLanguageCode(lang))
        else:
            executor = getattr(service, method)
        message = command["messages"][self.language]
        if(executor is not None):
            commandResult = executor(command["arg"])
        return self.getOutputSpeech(commandResult, message)


    def listenAndExecute(self, init=False):
        textResult = self.listen(init)
        output = None
        #not initial command
        if(textResult is not None):
            text = textResult.getResult()
            if(text is not None):
                output = self.execute(text)
            else:
                output = self.getOutputSpeech(textResult, '')
        self.speaker.speak(output, str(getCurrentTimestamp()) + ".mp3")
        #return output






