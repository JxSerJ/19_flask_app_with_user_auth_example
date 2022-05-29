from dao.movies import MovieDAO


class MovieService:
    def __init__(self, dao: MovieDAO):
        self.movie_dao = dao

    def get_all(self, director_id: int = None, genre_id: int = None, year: int = None):
        result_data = self.movie_dao.get_all(director_id=director_id, genre_id=genre_id, year=year)
        return result_data

    def get_one(self, movie_id: int):
        result_data = self.movie_dao.get_one(movie_id)
        return result_data

    def create(self, data):
        result_data = self.movie_dao.create(data)
        return result_data

    def update(self, movie_id: int, data):

        movie = self.movie_dao.get_one(movie_id)
        result_data = self.movie_dao.update(movie, data)
        return result_data

    def delete(self, movie_id: int):

        query = self.movie_dao.get_one(movie_id)
        self.movie_dao.delete(movie_id)
