from googletrans import Translator
import googletrans

from functools import lru_cache

from config.constants import OK
from services.action_result import ActionResult
from utils.utils import convert_list_to_str

class TranslationService:
    def __init__(self, language = "en"):
        self.__api = Translator()
        self.__language = language
        self.__buffered_text = None

    def set_language(self, language):
        self.__language = language

    def set_buffered_text(self, text):
        print("DEBUG")
        print(text)
        self.__buffered_text = text

    def get_buffered_text(self):
        return self.__buffered_text

    #high level service methods
    #@lru_cache(maxsize=32)
    def detect_language_from_text(self, text):
        lang_code = self.detect_language(text).lang
        return ActionResult(self.convert_lang_code_to_language(lang_code), OK)

    #NOTE:text must be in cyrillic for serbian
    def translate_text_with_auto_detection(self, text = None, dest_language = "en"):
        print(dest_language)
        text = text if text is not None else self.get_buffered_text()
        src_language = self.detect_language(text).lang
        if dest_language not in googletrans.LANGUAGES:
            dest_language = googletrans.LANGCODES.get(dest_language)
        return ActionResult(self.translate(text, src_lang=src_language, dest_lang=dest_language).text, OK)

    #low level service methods
    @lru_cache(maxsize=8)
    def translate(self, text, src_lang="en", dest_lang="en"):
        return self.__api.translate(text, src=src_lang, dest=dest_lang)
    @lru_cache(maxsize=8)
    def detect_language(self, text):
        return self.__api.detect(text)
    #TODO:handle possible exceptions
    def convert_language_to_lang_code(self, language):
        return googletrans.LANGCODES.get(language, "auto")
    def convert_lang_code_to_language(self, lang_code):
        #return googletrans.LANGUAGES.get(lang_code, "Undefined")
        return self.translate(googletrans.LANGUAGES.get(lang_code, "Undefined"), dest_lang=self.__language).text


'''
#https://py-googletrans.readthedocs.io/en/latest/
#https://pypi.org/project/gmail/
'''
