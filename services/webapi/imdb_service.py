import omdb
from config.constants import OMDB_API_KEY


# from functools  import lru_cache

class IMDBService:
    def __init__(self, api_key=OMDB_API_KEY):
        # self.api = omdb
        omdb.set_default('apikey', api_key)

    @property
    def api(self):
        return omdb

    def get_movie_by_title(self, title, year=None, fullplot=False, tomatoes=False):
        # timeout, page
        print(self.api.search(title))
        print(self.api.search_movie(title))
        print(self.api.get(title=title, fullplot=False, tomatoes=True))


#imdb = IMDBService()
#imdb.get_movie_by_title('Zikina dinastija VII')

# omdb.request(t='True Grit', y=1969, plot='full', tomatoes='true', timeout=5)
# Options
# https://github.com/dgilland/omdb.py
