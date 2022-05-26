from dao.model.genres import Genre


# CRUD
class GenreDAO:
    def __init__(self, session):
        self.session = session

    def get_all(self):

        result_data = self.session.query(Genre).all()
        return result_data

    def get_one(self, genre_id: int):

        result_data = self.session.query(Genre).filter(Genre.id == genre_id).one()
        return result_data

    def create(self, data):

        new_genre = Genre(**data)

        self.session.add(new_genre)
        self.session.commit()
        return new_genre

    def update(self, genre, data):

        for k, v in data.items():
            setattr(genre, k, v)
        self.session.add(genre)
        self.session.commit()
        return genre

    def delete(self, genre_id: int):

        genre = self.get_one(genre_id)
        self.session.delete(genre)
        self.session.commit()
