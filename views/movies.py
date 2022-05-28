from flask import request, jsonify
from flask_restx import Resource, Namespace

from helpers.decorators import auth_required, admin_required
from views.validator import validator
from marshmallow import ValidationError
from sqlalchemy.exc import NoResultFound

from container import movie_service
from dao.model.movies import MovieSchema, Movie

movies_ns = Namespace('movies')

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


@movies_ns.route('/')
class MoviesView(Resource):

    @auth_required
    def get(self):

        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')
        year = request.args.get('year')

        result_data = movie_service.get_all(director_id=director_id, genre_id=genre_id, year=year)

        if len(result_data) == 0:
            return "Data not found.", 404

        result = movies_schema.dump(result_data)
        return result, 200

    @admin_required
    def post(self):

        request_data = request.json
        try:
            validator("POST", request_data, Movie, movie_schema)
        except ValidationError as err:
            return err.messages, 400

        result_data = movie_service.create(request_data)

        result = movie_schema.dump(result_data)

        data_id = result["id"]

        response = jsonify(result)
        response.status_code = 201
        response.headers['location'] = f'/{movies_ns.name}/{data_id}'

        return response


@movies_ns.route('/<int:movie_id>')
class MovieView(Resource):

    @auth_required
    def get(self, movie_id: int):

        try:
            result_data = movie_service.get_one(movie_id)
        except NoResultFound:
            return f"Movie ID: {movie_id} not found", 404

        result = movie_schema.dump(result_data)
        return result, 200

    @admin_required
    def put(self, movie_id: int):

        request_data = request.json
        try:
            request_data = movie_schema.load(request_data)
        except ValidationError as err:
            return f"{err}", 400

        # check if all keys acquired
        schema_keys = set(movie_schema.fields.keys())
        schema_keys.remove('id')
        data_keys = request_data.keys()
        if 'id' in data_keys:
            data_keys = set(data_keys.remove('id'))
        else:
            data_keys = set(data_keys)
        if data_keys != schema_keys:
            return "Not all keys acquired", 400

        try:
            result_data = movie_service.update(movie_id, request_data)
        except NoResultFound:
            return f"Movie ID: {movie_id} not found", 404

        result = movie_schema.dump(result_data)
        return result, 200

    @admin_required
    def patch(self, movie_id: int):

        request_data = request.json
        try:
            request_data = movie_schema.load(request_data)
        except ValidationError as err:
            return f"{err}", 400

        try:
            result_data = movie_service.update(movie_id, request_data)
        except NoResultFound:
            return f"Movie ID: {movie_id} not found", 404

        result = movie_schema.dump(result_data)
        return result, 200

    @admin_required
    def delete(self, movie_id: int):

        try:
            movie_service.delete(movie_id)
        except NoResultFound:
            return f"Movie ID: {movie_id} not found", 404

        return f"Data ID: {movie_id} was deleted successfully.", 200
