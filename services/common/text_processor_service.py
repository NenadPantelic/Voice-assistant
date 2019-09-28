import string
from config.constants import ENGLISH_DICTIONARY_PATH, SERBIAN_DICTIONARY_PATH, logger
from utils.utils import load_words_dictionaries, flatten_lists

language_word_files = dict(en=ENGLISH_DICTIONARY_PATH, sr=SERBIAN_DICTIONARY_PATH)
word_dictionary_mapping = load_words_dictionaries(language_word_files)


class TextProcessor:
    def __init__(self, language="en"):
        self._language = language
        self._target_words = None
        self.set_language(language)

    # public methods
    def set_language(self, language):
        """
        Sets the language and target words based on language.
        :param str language: language code
        :rtype: None
        :return: void method (raise ValueError if language is not supported)
        """
        try:
            logger.debug("Text processor language = {}.".format(language))
            self._target_words = flatten_lists(word_dictionary_mapping[language].values())
            self._language = language
        except KeyError:
            raise ValueError("TextProcessor: Language is not supported. Use English or Serbian.")

    def preprocess_text(self, text):
        """
        Convert text to lowercase and filter out special chars (punctuation) and target words.
        :param str text: input text
        ":rtype: str
        :return: filter text with no punctuation marks and target words - usual words
        """
        text = text.lower()
        logger.debug("Text to be processed = {}".format(text))
        text_with_no_special_chars = self._filter_out_special_chars(text)
        logger.debug("Text without special chars = {}".format(text_with_no_special_chars))
        filtered_text = self._filter_out_words(text_with_no_special_chars)
        logger.debug("Text without target words = {}".format(filtered_text))
        return filtered_text

    def filter_out_keywords(self, word_list, keyword_list):
        """
        Filter out keywords from [word_list]. Keywords are stored in [keyword_list].
        :param word_list: list of words that needs to be filtered
        :param keyword_list: list of words that we want to filter out from [word_list]
        :rtype: str
        :return: string composed from words from [word_list] that do not belong to [keyword_list]
        """
        text_without_keywords = ' '.join([word for word in word_list if word not in keyword_list])
        logger.debug("Text without keywords = {}".format(text_without_keywords))
        return text_without_keywords

    # private methods
    def _filter_out_special_chars(self, phrase):
        """
        Removes punctuation from phrase.
        :param str phrase: Phrase that we want to process.
        :rtype: str
        :return: string phrase with no punctuation symbols.
        """
        return phrase.translate(str.maketrans("", "", string.punctuation))

    def _filter_out_words(self, phrase):
        """
        Filter out target words (usual words) from phrase.
        :param str phrase: input phrase.
        :rtype:  list of str
        :return: non-filtered list of words from phrase
        """
        word_list = phrase.split(' ')
        return [word for word in word_list if word.isalnum() and word not in self._target_words]
