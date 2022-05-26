from dao.directors import DirectorDAO
from dao.model.directors import DirectorSchema

director_schema = DirectorSchema()


class DirectorService:
    def __init__(self, dao: DirectorDAO):
        self.director_dao = dao

    def get_all(self):
        result_data = self.director_dao.get_all()
        return result_data

    def get_one(self, director_id: int):
        result_data = self.director_dao.get_one(director_id)
        return result_data

    def create(self, data):
        result_data = self.director_dao.create(data)
        return result_data

    def update(self, director_id: int, data):

        director = self.director_dao.get_one(director_id)
        result_data = self.director_dao.update(director, data)
        return result_data

    def delete(self, director_id: int):

        query = self.director_dao.get_one(director_id)
        self.director_dao.delete(director_id)
