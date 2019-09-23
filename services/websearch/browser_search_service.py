import threading
from functools import lru_cache
import googlesearch, webbrowser

from config.constants import OK, NO_GOOGLE_RESULT, FACEBOOK_BASE_URL, TWITTER_BASE_URL, INSTAGRAM_BASE_URL, LINKEDIN_BASE_URL
from services.action_result import ActionResult

TPE_MAP = {"videos": "vid", "images": "isch", "news": "nws", "shopping": "shop", "books": "bks", "applications": "app"}


class BrowserService:
    def __init__(self):
        self.__search = googlesearch.search


    @lru_cache(maxsize=16)
    def google_search(self, query, tld="com", tpe='vid', pause=2.0, stop=3):
        return self.__search(query=query, tld=tld, tpe=tpe, pause=pause, stop=stop)

    def get_first_search_result(self, query, tpe=''):
        results = self.google_search(query=query, tpe=tpe)
        # results is generator object
        # TODO:think about sequential search result acquiring - not only first result
        try:
            return ActionResult(next(results), OK)
        except StopIteration as e:
            # TODO logging
            return ActionResult(None, NO_GOOGLE_RESULT)

    def browser_open(self, url, new=2, autoraise=False):
        webbrowser.open(url, new=new, autoraise=autoraise)

    def browser_open_with_indep_thread(self, url):
        thread = threading.Thread(target=self.browser_open, args=(url,), daemon=True)
        thread.start()

    def open_found_url_in_browser(self, query, tpe = ''):
        google_result = self.get_first_search_result(query, tpe=tpe)
        url = google_result.get_result()
        if url is not None:
            self.browser_open(url=url)
            #thread = threading.Thread(target=self.browser_open, args=(url,), daemon=True)
            #thread.start()
            #return
        else:
            return ActionResult(None, NO_GOOGLE_RESULT)
        #thread.join()

    #this is tight coupled with controller logics, it asks for input
    def open_social_network_page(self, nickname = None, social_network_url = FACEBOOK_BASE_URL):
        url = social_network_url + nickname + "/"
        self.browser_open(url)
        #TODO:check return statements




