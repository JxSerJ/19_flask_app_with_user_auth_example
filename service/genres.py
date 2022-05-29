from dao.genres import GenreDAO


class GenreService:
    def __init__(self, dao: GenreDAO):
        self.genre_dao = dao

    def get_all(self):
        result_data = self.genre_dao.get_all()
        return result_data

    def get_one(self, genre_id: int):
        result_data = self.genre_dao.get_one(genre_id)
        return result_data

    def create(self, data):
        result_data = self.genre_dao.create(data)
        return result_data

    def update(self, genre_id: int, data):

        genre = self.genre_dao.get_one(genre_id)
        result_data = self.genre_dao.update(genre, data)
        return result_data

    def delete(self, genre_id: int):

        query = self.genre_dao.get_one(genre_id)
        self.genre_dao.delete(genre_id)
