import wikipedia

from ..action_result import ActionResult
from utils.utils import  loggingException
from config.constants import *
from functools import lru_cache
#print (wikipedia.summary("Wikipedia"))
#print(wikipedia.search('Novak'))

nd = wikipedia.page('Nikola Tesla')
#print(nd.title)
#print(nd.url)
#print(nd.content)
#print(nd.links)
#print(wikipedia.summary('Nikola Tesla'))
wikipedia.set_lang("sr")
#print(wikipedia.summary('Nikola Tesla'))

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
        if(language is not None):
            self.changeLanguage(language)

    def changeLanguage(self, language):
        wikipedia.set_lang(language)

    @lru_cache(maxsize=32)
    def briefSearch(self, query, sentences = 3):
        try:
            return  ActionResult(wikipedia.summary(query, sentences=sentences), OK)
        except Exception as e:
            loggingException(e)
            return ActionResult(e, DEFAULT_EXCEPTION)

    @lru_cache(maxsize=32)
    def getCompletePage(self, query):
        try:
            page = wikipedia.page(query)
            return  ActionResult(page.content, OK)
        except Exception as e:
            loggingException(e)
            return ActionResult(e, DEFAULT_EXCEPTION)



