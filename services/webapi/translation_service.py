from googletrans import Translator
import googletrans

from functools import lru_cache
from config.constants import SUCCESS
from services.action_result import ActionResult
from utils.utils import load_json_data, convert_latinic_to_cyrilic
from config.constants import LANGUAGES_IN_SERBIAN


class TranslationService:
    def __init__(self, language="en"):
        self.__api = Translator()
        self.__language = language
        self.__langs_in_serbian = load_json_data(LANGUAGES_IN_SERBIAN)

    def set_language(self, language):
        self.__language = language

    # high level service methods
    # @lru_cache(maxsize=32)
    # in this use-case, this method has no much sense, because speech recognizer needs to know language for recongition
    def detect_language_from_text(self, text):
        lang_code = self.detect_language(text).lang
        return ActionResult(self.convert_lang_code_to_language(lang_code), SUCCESS)

    # NOTE:text must be in cyrillic for serbian
    def translate_text(self,  text=None, src_language=None, dest_language="en"):
        #text = text if text is not None else self.get_buffered_text()
        #if src_language is None:
        #    src_language = self.get_src_language() if self.get_src_language() else self.detect_language_from_text(text)
        print("DEBUG: src = ",src_language, dest_language)
        dest_language = self.get_appropriate_lang_code(dest_language)
        # TODO: handle speaking in destination language, not language set in controller
        return ActionResult(self.translate(text, src_lang=src_language, dest_lang=dest_language).text, SUCCESS,
                            language=dest_language)

    # low level service methods
    @lru_cache(maxsize=8)
    def translate(self, text, src_lang="en", dest_lang="en"):
        return self.__api.translate(text, src=src_lang, dest=dest_lang)

    @lru_cache(maxsize=8)
    def detect_language(self, text):
        return self.__api.detect(text)

    # TODO:handle possible exceptions
    def convert_language_to_lang_code(self, language):
        return googletrans.LANGCODES.get(language, "en")

    def convert_lang_code_to_language(self, lang_code):
        # return googletrans.LANGUAGES.get(lang_code, "Undefined")
        return self.translate(googletrans.LANGUAGES.get(lang_code, "english"), dest_lang=self.__language).text

    # TODO:think about conversion to cyrillic when using serbian
    def get_appropriate_lang_code(self, language):
        if self.__language == 'sr':
            language = convert_latinic_to_cyrilic(language)
            language = self.__langs_in_serbian.get(language, "en")
        if language not in googletrans.LANGUAGES:
            language = self.convert_language_to_lang_code(language)
        return language


'''
#https://py-googletrans.readthedocs.io/en/latest/
#https://pypi.org/project/gmail/
'''
