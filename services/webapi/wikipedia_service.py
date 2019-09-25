import wikipedia
from services.action_result import ActionResult
from utils.utils import logging_exception
from config.constants import *
from functools import lru_cache
'''
# print (wikipedia.summary("Wikipedia"))
# print(wikipedia.search('Novak'))

nd = wikipedia.page('Nikola Tesla')
# print(nd.title)
# print(nd.url)
# print(nd.content)
# print(nd.links)
# print(wikipedia.summary('Nikola Tesla'))
wikipedia.set_lang("sr")
# print(wikipedia.summary('Nikola Tesla'))

'''
'''
>>> wikipedia.search("Barack")
# [u'Barak (given name)', u'Barack Obama', u'Barack (brandy)', u'Presidency of Barack Obama', u'Family of Barack Obama', u'First inauguration of Barack Obama', u'Barack Obama presidential campaign, 2008', u'Barack Obama, Sr.', u'Barack Obama citizenship conspiracy theories', u'Presidential transition of Barack Obama']

>>> ny = wikipedia.page("New York")
>>> ny.title
# u'New York'
>>> ny.url
# u'http://en.wikipedia.org/wiki/New_York'
>>> ny.content
# u'New York is a state in the Northeastern region of the United States. New York is the 27th-most exten'...
>>> ny.links[0]
# u'1790 United States Census'

>>> wikipedia.set_lang("fr")
>>> wikipedia.summary("Facebook", sentences=1)
# Facebook est un service de réseautage social en ligne sur Internet permettant d'y publier des informations (phot
'''


class WikipediaService:
    def __init__(self, language="en"):
        if language is not None:
            self.set_language(language)

    def set_language(self, language):
        """
        Sets language of wikipedia client API
        :param language (str): language code
        :return:
        """
        wikipedia.set_lang(language)

    @lru_cache(maxsize=8)
    def brief_search(self, query, sentences=3):
        """
        Get summary section of page that satisfy query.
        :param query(str): searching term
        :param sentences: number of sentences that wikipedia summary should have
        :return: ActionResult with the result from wikipedia page (or appropriate error message)
        """
        if sentences > 10: raise ValueError("Number of summary sentences can not be greater than 10.")
        return ActionResult(wikipedia.summary(query, sentences=sentences), SUCCESS)

    #not tested nor used
    @lru_cache(maxsize=8)
    def get_complete_page(self, query):
        """
        Returns wiki page that satisfy input query (complete page content)
        :param query(str): searching term
        :return:
        """
        try:
            page = wikipedia.page(query)
            return ActionResult(page.content, SUCCESS)
        except Exception as e:
            logging_exception(e)
            return ActionResult(e, DEFAULT_EXCEPTION)
