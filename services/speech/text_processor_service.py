import logging
import string

from config.constants import ENGLISH_DICTIONARY_PATH, SERBIAN_DICTIONARY_PATH, ENGLISH_KEYWORDS
from utils.utils import load_words_dictionaries, flatten_lists, load_json_data

languageWordFiles = dict(en=ENGLISH_DICTIONARY_PATH, sr=SERBIAN_DICTIONARY_PATH)
keywordsFiles = dict(en=ENGLISH_KEYWORDS)


wordDictionaryMapping = load_words_dictionaries(languageWordFiles)

keywords = {lang:load_json_data(keywordsFiles[lang]) for lang in keywordsFiles}


class TextProcessor:
    def __init__(self, language="en"):
        self.__language = language
        self.__target_words = None
        self.set_language(language)

    def set_language(self, language):
        try:
            self.__target_words = flatten_lists(wordDictionaryMapping[language].values())
            self.__language = language
        except KeyError:
            logging.debug("Language is not supported. Use English or Serbian.")

    # @staticmethod
    def filter_out_special_chars(self, phrase):
        return phrase.translate(str.maketrans("", "", string.punctuation))

    def filter_out_words(self, phrase):
        wordList = phrase.lower().split(' ')
        return [word for word in wordList if word.isalpha() and word not in self.__target_words]

    def preprocess_text(self, text):
        return self.filter_out_words(self.filter_out_special_chars(text))

    def filter_out_keywords(self, phraseList, keywordList):
        return ' '.join([word for word in phraseList if word not in keywordList])
