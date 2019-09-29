from googletrans import Translator
import googletrans

from functools import lru_cache
from config.config import SUCCESS, logger
from services.common.action_result import ActionResult
from utils.utils import load_json_data, convert_latin_to_cyrillic
from config.config import LANGUAGES_IN_SERBIAN


class TranslationService:
    def __init__(self, language="en"):
        self._api = Translator()
        self._language = language
        #TODO:this field is tight coupled with serbian _language usage logic, solve that
        self._langs_in_serbian = load_json_data(LANGUAGES_IN_SERBIAN)

    # public methods
    def set_language(self, language):
        """
        Sets operating _language of translation service.
        :param str language: _language code
        :rtype:None
        :return: void method (no return value)
        """
        assert(isinstance(language, str))
        self._language = language

    # in this use-case, this method has no much sense, because speech _recognizer needs to know _language for recongition
    def detect_language_from_text(self, text):
        """
        Detects _language from text.
        :param str text: text to be analyzed
        :rtype ActionResult
        :return: ActionResult with _language name as payload
        """
        assert(isinstance(text, str))
        lang_code = self._detect_language(text).lang
        return ActionResult(self._convert_lang_code_to_language(lang_code), SUCCESS)

    # NOTE:text must be in cyrillic for serbian, latin is for croatian
    def translate_text(self,  text=None, src_language="en", dest_language="en"):
        """
        Translates text from src_language to dest_language.If text is `Mary had a little lamb`, src_language `en`, and
        dest_language is `sr`, resulting text has value: `Мери је имала мало јагње`
        :param str text: text for translation
        :param str src_language: _language code of text's _language
        :param str dest_language: target translation _language
        :rtype ActionResult
        :return: ActionResult with translated text as payload
        """
        assert(isinstance(text, str) and isinstance(src_language, str) and isinstance(dest_language, str))
        logger.debug("Calling translate_text with params: [text = {}, src_language = {}, dest_language = {}]".
                     format(text, src_language, dest_language))
        dest_language = self._get_appropriate_lang_code(dest_language)
        logger.debug("Language code = {}.".format(dest_language))
        translated_text = self._translate(text, src_lang=src_language, dest_lang=dest_language)
        logger.debug("Raw translation object = {}".format(translated_text))
        logger.debug("Translated text = {}".format(translated_text.text))
        return ActionResult(translated_text.text, SUCCESS, language=dest_language)

    #private methods
    @lru_cache(maxsize=8)
    def _translate(self, text, src_lang="en", dest_lang="en"):
        """
        Translates text by using Google Translate API.
        :param str text: text for translation
        :param str src_language: _language code of text's _language
        :param str dest_language: target translation _language
        :rtype googletrans.models.Translated object
        :return: translated object
        """
        assert(isinstance(text, str) and isinstance(src_lang, str) and isinstance(dest_lang, str))
        return self._api.translate(text, src=src_lang, dest=dest_lang)

    @lru_cache(maxsize=8)
    def _detect_language(self, text):
        """
         Detect _language of the input text

        :param text: The source text(s) whose _language you want to identify.
                     Batch detection is supported via sequence input.
        :type_ text: UTF-8 :class:`str`; :class:`unicode`; string sequence (list, tuple, iterator, generator)

        :rtype: Detected
        :return: Detected object
        """
        assert(isinstance(text, str))
        return self._api.detect(text)

    # helper methods
    #TODO:move these methods to utils
    def _convert_language_to_lang_code(self, language):
        """
        Converts and returns _language code for the given _language. If _language is not valid, default value is `en`.
        :param str language: full _language name, e.g. english,serbian, italian...
        :rtype str
        :return: _language code, e.g. `en` for english, `it` for italian, `sr` for serbian
        """
        assert(isinstance(language, str))
        return googletrans.LANGCODES.get(language, "en")

    # not used at the moment
    def _convert_lang_code_to_language(self, lang_code):
        '''
        Convert the given _language code to _language name. `sr` to serbian, `en` to english etc.
        :param str lang_code:
        :rtype str
        :return: correspongin _language name or `english` if lang_code is not valid.
        '''
        assert(isinstance(lang_code, str))
        return self._translate(googletrans.LANGUAGES.get(lang_code, "english"), dest_lang=self._language).text

    def _get_appropriate_lang_code(self, language):
        """
        Determines and returns the corresponding lang_code.
        :param str language: _language or _language code
        :rtype str
        :return:lang_code of the given _language
        """
        assert(isinstance(language, str))
        logger.debug("Getting appropriate _language code...")
        if self._language == 'sr':
            language = convert_latin_to_cyrillic(language)
            language = self._langs_in_serbian.get(language, "en")
        if language not in googletrans.LANGUAGES:
            language = self._convert_language_to_lang_code(language)
        return language



