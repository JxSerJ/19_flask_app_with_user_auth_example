from dao.model.directors import Director


# CRUD
class DirectorDAO:
    def __init__(self, session):
        self.session = session

    def get_all(self):

        result_data = self.session.query(Director).all()
        return result_data

    def get_one(self, director_id: int):

        result_data = self.session.query(Director).filter(Director.id == director_id).one()
        return result_data

    def create(self, data):

        new_director = Director(**data)

        self.session.add(new_director)
        self.session.commit()
        return new_director

    def update(self, director, data):

        for k, v in data.items():
            setattr(director, k, v)
        self.session.add(director)
        self.session.commit()
        return director

    def delete(self, director_id: int):

        director = self.get_one(director_id)
        self.session.delete(director)
        self.session.commit()
