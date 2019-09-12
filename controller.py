from services import *
from config.constants import *


class Controller:
    def __init__(self, recognizer, speaker, semanticProcessor, executor=None, servicePool={}):
        self.recognizer = recognizer
        self.speaker = speaker
        self.executor = executor
        self.semanticProcessor = semanticProcessor
        self.servicePool = servicePool
        self.language = None

    def switchLanguage(self, language):
        assert isinstance(language, str) and language in PROVIDED_LANGUAGES
        self.language = language
