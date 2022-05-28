import os

from flask import Flask
from flask_restx import Api

from database.set_db import db
from database.create_main_db import create_data
from database.create_user_db import create_user_data

from views.movies import movies_ns
from views.directors import directors_ns
from views.genres import genres_ns
from views.users import users_ns
from views.auth import auth_ns

from config import Config


def create_app(config_obj):
    app = Flask(__name__)
    app.config.from_object(config_obj)
    initialize_extensions(app)
    return app


def initialize_extensions(app):
    db.init_app(app)

    api = Api(app)
    api.add_namespace(movies_ns)
    api.add_namespace(directors_ns)
    api.add_namespace(genres_ns)
    api.add_namespace(users_ns)
    api.add_namespace(auth_ns)

    if not app.debug or os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        if Config.REGENERATE_DB_ON_START:
            with app.app_context():
                create_user_data(db)
                create_data(db)
        else:
            print("Database regeneration skipped! You're now using database saved on storage.")


if __name__ == '__main__':
    application = create_app(Config)
    application.run(host='localhost', port=5000)
