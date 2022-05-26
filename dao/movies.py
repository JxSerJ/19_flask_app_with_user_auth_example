from dao.model.movies import Movie


# CRUD
class MovieDAO:
    def __init__(self, session):
        self.session = session

    def get_all(self, director_id: int = None, genre_id: int = None, year: int = None):

        query = self.session.query(Movie)

        if director_id:
            query = query.filter(Movie.director_id == director_id)
        if genre_id:
            query = query.filter(Movie.genre_id == genre_id)
        if year:
            query = query.filter(Movie.year == year)

        result_data = query.all()
        return result_data

    def get_one(self, movie_id: int):

        result_data = self.session.query(Movie).filter(Movie.id == movie_id).one()
        return result_data

    def create(self, data):

        new_movie = Movie(**data)

        self.session.add(new_movie)
        self.session.commit()
        return new_movie

    def update(self, movie, data):

        for k, v in data.items():
            setattr(movie, k, v)
        self.session.add(movie)
        self.session.commit()
        return movie

    def delete(self, movie_id: int):

        movie = self.get_one(movie_id)
        self.session.delete(movie)
        self.session.commit()
