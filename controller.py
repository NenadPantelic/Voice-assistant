from services import *
from config.constants import *
from utils.utils import loadJsonData

from services.websearch import wikipedia_search
#from services.websearch import * #import WikipediaService


commands = loadJsonData(ENGLISH_COMMANDS)


servicePool = {

    "wikipedia": wikipedia_search.WikipediaService(language=None)

}

class Controller:
    def __init__(self, recognizer, speaker, commandResolver, executor=None, servicePool={}):
        self.recognizer = recognizer
        self.speaker = speaker
        self.executor = executor
        self.executingMethod = None
        self.commandResolver = commandResolver
        self.servicePool = servicePool
        self.language = None

    def switchLanguage(self, language):
        assert isinstance(language, str) and language in PROVIDED_LANGUAGES
        self.language = language


    def determineExecutor(self, text):
        serviceMethod = self.commandResolver.getCommand(text)
        #self.executor = servicePool[serviceMethod["service"]]
        #self.executingMethod = getattr(self.executor, serviceMethod["method"])
        #arg = serviceMethod["arg"]
        #response = self.speak(serviceMethod["service"] + '-' + serviceMethod["method"]) + str(self.executingMethod(arg).getResult())
        #return response
        print(serviceMethod)
        return serviceMethod







