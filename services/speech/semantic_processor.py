import logging
import string

from config.constants import ENGLISH_DICTIONARY_PATH, SERBIAN_DICTIONARY_PATH
from utils.utils import loadWordsDictionaries, flattenDictionaryValues

languageWordFiles = dict(en=ENGLISH_DICTIONARY_PATH, sr=SERBIAN_DICTIONARY_PATH)
wordDictionaryMapping = loadWordsDictionaries(languageWordFiles)


class SemanticProcessor:
    def __init__(self, language="en"):
        self.__language = language
        self.__targetWords = None
        self.setLanguage(language)

    def setLanguage(self, language):
        try:
            self.__targetWords = flattenDictionaryValues(wordDictionaryMapping["en"].values())
            self.__language = language
        except KeyError:
            logging.debug("Language is not supported. Use English or Serbian.")

    # @staticmethod
    def filterOutSpecialChars(self, phrase):
        return phrase.translate(str.maketrans("", "", string.punctuation))

    def filterOutWords(self, phrase):
        wordList = phrase.lower().split(' ')
        return " ".join([word for word in wordList if word.isalpha() and word not in self.__targetWords])
