import json

from flask import current_app

from constants import INITIAL_DATA_PATH
from dao.model.movies import Movie
from dao.model.directors import Director
from dao.model.genres import Genre


def create_data(db):

    try:
        with current_app.app_context():
            db.drop_all()
            db.create_all()

            with open(INITIAL_DATA_PATH, 'r', encoding='UTF-8') as file:
                file_data = json.load(file)

            new_movies = []
            new_genres = []
            new_directors = []

            for entry in file_data['movies']:
                new_movies.append(Movie(**entry))

            for entry in file_data['genres']:
                new_genres.append(Genre(**entry))

            for entry in file_data['directors']:
                new_directors.append(Director(**entry))

            db.session.add_all(new_movies)
            db.session.add_all(new_genres)
            db.session.add_all(new_directors)
            db.session.commit()
            db.session.close()

        print("\nDatabase regenerated successfully!")

    except Exception as err:
        print(f"Database error: {err} \n\n"
              f"Database regeneration incomplete. Data may be corrupted!")
