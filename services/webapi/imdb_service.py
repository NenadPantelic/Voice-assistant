import omdb, imdb
from config.constants import OMDB_API_KEY, SUCCESS

# from functools  import lru_cache
from services.action_result import ActionResult


class IMDBService:
    def __init__(self, api_key=OMDB_API_KEY):
        # self.api = omdb
        omdb.set_default('apikey', api_key)
        self.__imdb = imdb.IMDb()

    @property
    def api(self):
        return omdb

    # high level
    def get_top_movies(self, num=1):
        #assert(isinstance(num, int)), "Value must be integer by type."
        #if num not in range(1, 251):
        #    raise ValueError("Value must be in range 1 to 250")
        #TODO:handle num when spoken in Serbian, it uses words, in english it uses numbers
        if(num == "jedan"): num = 1
        num = int(num)
        top_movies = self.__imdb.get_top250_movies()[:num]
        complete_info = ""
        for movie in top_movies:
            movie_id = self.get_movie_id(movie)
            movie_details = self.get_movie_by_id(movie_id)
            movie_info = self.get_brief_movie_info(movie_details)
            complete_info += self.movie_info_to_str(movie_info) + "\n"
        return ActionResult(complete_info, SUCCESS, language="en")

    def get_movie_details(self, title):
        movie = self.get_first_movie(title)
        if movie is not None:
            movie_id = self.get_movie_id(movie)
            movie_details = self.get_movie_by_id(movie_id)
            movie_info = self.get_detailed_movie_info(movie_details)
            return ActionResult(self.movie_info_to_str(movie_info), SUCCESS, language="en")
        else:
            return None

    # low level
    # imdb methods
    def get_movies_by_title(self, title):
        return self.__imdb.search_movie(title)

    def get_first_movie(self, title, position=0):
        movies = self.get_movies_by_title(title)
        return movies[0] if len(movies) > 0 else None

    def get_movie_id(self, movie):
        return movie.movieID

    def get_movie_by_place(self, movies, place=0):
        return movies[place]

    # omdb
    # id is numerical string, IMDB id should be in form tt<numerical_id>
    def get_movie_by_id(self, id):
        return self.api.imdbid("tt" + id)

    def get_movie_info(self, movie, info_props):
        movie_info = {}
        for property in info_props:
            movie_info[property] = movie[property]
        return movie_info

    def get_brief_movie_info(self, movie):
        info_props = ("title", "genre", "imdb_rating")
        return self.get_movie_info(movie, info_props)

    def get_detailed_movie_info(self, movie):
        info_props = (
            "title", "year", "released", "runtime", "genre", "director", "actors", "plot", "language", "imdb_rating")
        return self.get_movie_info(movie, info_props)

    def movie_info_to_str(self, movie_info):
        info_str = ""
        for property_name, property_value in movie_info.items():
            info_str += property_name + ": " + property_value + ",\n"
        return info_str

    def get_movie_by_title(self, title, year=None, fullplot=False, tomatoes=False):
        # timeout, page
        # print(self.api.search(title))
        # print(self.api.search_movie(title))
        print(self.api.get(title=title, fullplot=False, tomatoes=True))

# imdb.get_movie_by_title('Zikina dinastija VII')

# omdb.request(t='True Grit', y=1969, plot='full', tomatoes='true', timeout=5)
# Options
# https://github.com/dgilland/omdb.py

# import imdb
# ia = imdb.IMDb()
# movies = ia.search_movie('Lepa sela lepo gore')
# print(movies)
##omdb_ser = IMDBService()
# id = movies[0].movieID
# print(omdb_ser.get_movie_by_id("tt" + id))
#https://imdbpy.readthedocs.io/en/latest/usage/quickstart.html#searching