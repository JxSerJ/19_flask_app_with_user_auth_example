from database.set_db import db

from dao.movies import MovieDAO
from dao.directors import DirectorDAO
from dao.genres import GenreDAO

from service.movies import MovieService
from service.directors import DirectorService
from service.genres import GenreService


movie_dao = MovieDAO(db.session)
movie_service = MovieService(dao=movie_dao)

director_dao = DirectorDAO(db.session)
director_service = DirectorService(dao=director_dao)

genre_dao = GenreDAO(db.session)
genre_service = GenreService(dao=genre_dao)
