import imdb
import omdb

from config.constants import OMDB_API_KEY, SUCCESS, logger
from functools import lru_cache
from services.common.action_result import ActionResult


class IMDBService:
    def __init__(self, api_key=OMDB_API_KEY):
        omdb.set_default('apikey', api_key)
        self.__imdb = imdb.IMDb()
        self._language = "en"

    @property
    def _api(self):
        return omdb

    # public methods
    @lru_cache(maxsize=8)
    def get_top_movies(self, num=1):
        """
        Returns brief movie info details about best movies by imdb. Number of movies is determined by [num] arg. This
        argument cannot be greater than 250.
        :param num: Number of top movies we seek. (int); in range [1,250]
        :return: movies info string wrapped in ActionResult; default speaking language is english
        """
        assert (isinstance(num, int)), "Value must be integer by type_."
        assert (num in range(1, 251)), "Value must be in range 1 to 250"
        # TODO:handle num when spoken in Serbian, it uses words, in english it uses numbers
        num = int(num)
        logger.debug("Seeking for best movies by imdb. Params: [num = {}].".format(num))
        top_movies = self.__imdb.get_top250_movies()[:num]
        complete_info = ""
        for movie in top_movies:
            movie_id = self._get_movie_id(movie)
            logger.debug("Movie id = {}".format(movie_id))
            movie_details = self._get_movie_by_id(movie_id)
            movie_info = self._get_brief_movie_info(movie_details)
            complete_info += self._movie_info_to_str(movie_info) + "\n"
        logger.debug("Complete movies info:\n{}".format(complete_info))
        #NOTE:action result language is set to english because imdb API results are in english
        return ActionResult(complete_info, SUCCESS, language="en")

    @lru_cache(maxsize=8)
    def get_movie_details(self, title):
        """
        Get movie details (full form) for movie with title [title].
        :param title: Movie title (str)
        :return: Movie details (str) wrapped in ActionResult.
        """
        assert (isinstance(title, str))
        logger.debug("Get movie details. Params: [title = {}].".format(title))
        movie = self._get_first_movie(title)
        if movie is not None:
            movie_id = self._get_movie_id(movie)
            logger.debug("Movie id = {}".format(movie_id))
            movie_details = self._get_movie_by_id(movie_id)
            if movie_details != {}:
                movie_info = self._get_detailed_movie_info(movie_details)
                movie_info_rdbl_form = self._movie_info_to_str(movie_info)
                logger.debug("Complete movie info:\n{}".format(movie_info))
            else:
                movie_info_rdbl_form = "Movie that you asked for cannot be found."
                logger.debug("Movie cannot be found....")
            return ActionResult(movie_info_rdbl_form, SUCCESS, language="en")
        else:
            return None

    # private methods
    # imdb methods
    def _get_movies_by_title(self, title):
        """
        Returns list of movies (imdb.Movie.Movie) that suits [title] argument
        :param title: Movie title (str)
        :return:
        """
        assert (isinstance(title, str))
        logger.debug("Searching for movies with title = {}.".format(title))
        return self.__imdb.search_movie(title)

    def _get_first_movie(self, title):
        """
        Returns first fetched movie (if there is any).
        :param title: Movie title (str)
        :return: imdb.Movie.Movie object
        """
        assert (isinstance(title, str))
        movies = self._get_movies_by_title(title)
        logger.debug("Movies fetching is over.")
        return movies[0] if len(movies) > 0 else None

    def _get_movie_id(self, movie):
        """
        Returns movie id.
        :param movie: imdb.Movie.Movie object
        :return: movie id (on imdb) (str)
        """
        assert (isinstance(movie, imdb.Movie.Movie))
        return movie.movieID

    # omdb
    def _get_movie_by_id(self, _id):
        """
        Returns dicionary with movie details.
        :param _id: movie id by imdb (str) - id is numerical string, IMDB id should be in form tt<numerical_id>
        :return:
        """
        assert (isinstance(_id, str))
        return self._api.imdbid("tt" + _id)

    def _get_movie_info(self, movie, info_props):
        """
        Returns movie info - parameters that are used in info are described in info_props tuple.
        :param movie: dictionary with movie details
        :param info_props: tuple with parameters for info
        :return: dictionary that contains parameters from info_props as keys
        """
        assert (isinstance(movie, dict))
        assert (isinstance(info_props, tuple))
        movie_info = {}
        logger.debug("Creating movie info....")
        for property in info_props:
            movie_info[property] = movie[property]
        return movie_info

    def _get_brief_movie_info(self, movie):
        """
        Getting info in brief form - dictionary with keys from info_props
        :param movie: movie description dictionary
        :return: dictionary with params from info_props as keys
        """
        assert (isinstance(movie, dict))
        info_props = ("title", "genre", "imdb_rating")
        return self._get_movie_info(movie, info_props)

    def _get_detailed_movie_info(self, movie):
        """
        Getting info in detailed form - dictionary with keys from info_props
        :param movie: movie description dictionary
        :return: dictionary with params from info_props as keys
       """
        assert (isinstance(movie, dict))
        info_props = (
            "title", "year", "released", "runtime", "genre", "director", "actors", "plot", "language", "imdb_rating")
        return self._get_movie_info(movie, info_props)

    def _movie_info_to_str(self, movie_info):
        """
        Returns movie info details in string form - param: value\n
        :param movie_info:
        :return:
        """
        assert (isinstance(movie_info, dict))
        info_str = ""
        for property_name, property_value in movie_info.items():
            info_str += property_name + ": " + property_value + ",\n"
        return info_str

