import sys
sys.path.append("..")
from services.webapi.imdb_service import IMDBService
imdb = IMDBService()
print(imdb.get_top_movies(num=10).get_result())
print(imdb.get_movie_details("Don Corleone").get_result())
print(imdb.get_movie_details("Deer hunter").get_result())
print(imdb.get_movie_details("Tesna koža").get_result())

# https://imdbpy.readthedocs.io/en/latest/usage/quickstart.html#searching
