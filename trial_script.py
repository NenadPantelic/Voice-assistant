# search(query, tld='com', lang='en', num=10, start=0, stop=None, pause=2.0)
'''

query : query string that we want to search for.
tld : tld stands for top level domain which means we want to search our result on google.com or google.in or some other domain.
lang : lang stands for language.
num : Number of results we want.
start : First result to retrieve.
stop : Last result to retrieve. Use None to keep searching forever.
pause : Lapse to wait between HTTP requests. Lapse too short may cause Google to block your IP. Keeping significant lapse will make your program slow but its safe and better option.
Return : Generator (iterator) that yields found URLs. If the stop parameter is None the iterator will loop forever.
'''

# import googlesearch
from config.constants import SUCCESS, NO_GOOGLE_RESULT, FACEBOOK_BASE_URL
from services.action_result import ActionResult

'''
try:
    from googlesearch import search
except ImportError:
    print("No module named 'google' found")

# to search
query = "Geeksforgeeks"

for j in search(query, tld="com", num=10, stop=1, pause=2):
    print(j)
'''
j = 'https://www.geeksforgeeks.org/'
j = "https://www.youtube.com/watch?v=6QU_nX4Y9Nw"
import threading

# https://python-googlesearch.readthedocs.io/en/latest/

# https://docs.python.org/2/library/webbrowser.html

'''
webbrowser.open(url, new=1, autoraise=True)
Display url using the default browser. If new is 0, the url is opened in the same browser window if possible. If new is 1, a new browser window is opened if possible. If new is 2, a new browser page (“tab”) is opened if possible. If autoraise is True, the window is raised if possible (note that under many window managers this will occur regardless of the setting of this variable).

Note that on some platforms, trying to open a filename using this function, may work and start the operating system’s associated program. However, this is neither supported nor portable.

Changed in version 2.5: new can now be 2.

webbrowser.open_new(url)
Open url in a new window of the default browser, if possible, otherwise, open url in the only browser window.

webbrowser.open_new_tab(url)
Open url in a new page (“tab”) of the default browser, if possible, otherwise equivalent to open_new().

New in version 2.5.

'''

import webbrowser
import time


def open_url(url, new, autoraise=False):
    webbrowser.open(url, new=2, autoraise=False)
    time.sleep(5)


def open_window(url):
    webbrowser.open_new(url)


def open_tab(url):
    webbrowser.open_tab(url)

# https://realpython.com/intro-to-python-threading/

from functools import lru_cache
import googlesearch

TPE_MAP = {"videos": "vid", "images": "isch", "news": "nws", "shopping": "shop", "books": "bks", "applications": "app"}


class BrowserService:
    def __init__(self):
        self.__search = googlesearch.search
        self.__last_searched_term = None
        self.__last_searched_type = None
        self.__thread_counter = 0

    # NOTE:maybe tpe property of search can be used
    def set_tpe(self, tpe):
        tpe = TPE_MAP.get(tpe, '')

    @lru_cache(maxsize=16)
    def google_search(self, query, tld="com", tpe='vid', pause=2.0, stop=3):
        self.__last_searched_term = query
        self.__last_searched_type = tpe
        return self.__search(query=query, tld=tld, tpe=tpe, pause=pause, stop=stop)

    def get_first_search_result(self, query, tpe=''):
        results = self.google_search(query=query, tpe=tpe)
        # results is generator object
        # TODO:think about sequential search result acquiring - not only first result
        try:
            return ActionResult(next(results), SUCCESS)
        except StopIteration as e:
            # TODO logging
            return ActionResult(None, NO_GOOGLE_RESULT)

    # TODO:enable multiparam execution of methods in controller

    def browser_open(self, url, new=2, autoraise=False):
        webbrowser.open(url, new=new, autoraise=autoraise)

    def browser_open_with_indep_thread(self, url):
        thread = threading.Thread(target=self.browser_open, args=(url,), daemon=True)
        thread.start()

    def open_found_url_in_browser(self, query):
        google_result = self.get_first_search_result(query)
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
        if nickname is None:
            nickname = input()
        url = social_network_url + nickname + "/"
        self.browser_open(url)
        #TODO:check return statements



