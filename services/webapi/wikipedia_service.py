import wikipedia
from services.common.action_result import ActionResult
from utils.utils import logging_exception
from config.constants import logger, SUCCESS, DEFAULT_EXCEPTION
from functools import lru_cache

class WikipediaService:
    def __init__(self, language="en"):
        if language is not None:
            self.set_language(language)

    def set_language(self, language):
        """
        Sets language of wikipedia client API
        :param language: language code (str)
        :return:
        """
        logger.debug("Setting wikipedia language: {}".format(language))
        wikipedia.set_lang(language)

    @lru_cache(maxsize=8)
    def brief_search(self, query, sentences=3):
        """
        Get summary section of page that satisfy query.
        :param query: searching term  (str)
        :param sentences: number of sentences that wikipedia summary should have (int)
        :return: ActionResult with the result from wikipedia page (or appropriate error message)
        """
        logger.debug("Calling wikipedia brief_search with [query = {}]".format(query))
        if sentences > 10: raise ValueError("Number of summary sentences can not be greater than 10.")
        summary = wikipedia.summary(query, sentences=sentences)
        logger.debug("Wikipedia summary = {}".format(summary))
        return ActionResult(summary, SUCCESS)

    #not tested nor used
    @lru_cache(maxsize=8)
    def get_complete_page(self, query):
        """
        Returns wiki page that satisfy input query (complete page content)
        :param query: searching term (str)
        :return:
        """
        try:
            page = wikipedia.page(query)
            return ActionResult(page.content, SUCCESS)
        except Exception as e:
            logging_exception(e)
            return ActionResult(e, DEFAULT_EXCEPTION)
