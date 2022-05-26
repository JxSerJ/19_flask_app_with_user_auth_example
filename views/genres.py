from flask import request, jsonify
from flask_restx import Resource, Namespace
from views.validator import validator
from marshmallow import ValidationError
from sqlalchemy.exc import NoResultFound

from container import genre_service
from dao.model.genres import GenreSchema, Genre

genres_ns = Namespace('genres')

genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)


@genres_ns.route('/')
class GenresView(Resource):

    def get(self):

        result_data = genre_service.get_all()
        if len(result_data) == 0:
            return "Data not found. Empty database.", 404

        result = genres_schema.dump(result_data)
        return result, 200

    def post(self):

        request_data = request.json
        try:
            validator("POST", request_data, Genre, genre_schema)
        except ValidationError as err:
            return err.messages, 400

        result_data = genre_service.create(request_data)

        result = genre_schema.dump(result_data)

        data_id = result["id"]

        response = jsonify(result)
        response.status_code = 201
        response.headers['location'] = f'/{genres_ns.name}/{data_id}'

        return response


@genres_ns.route('/<int:genre_id>')
class GenreView(Resource):

    def get(self, genre_id: int):

        try:
            result_data = genre_service.get_one(genre_id)
        except NoResultFound:
            return f"Genre ID: {genre_id} not found", 404

        result = genre_schema.dump(result_data)
        return result, 200

    def put(self, genre_id: int):

        request_data = request.json
        try:
            request_data = genre_schema.load(request_data)
        except ValidationError as err:
            return f"{err}", 400

        # check if all keys acquired
        schema_keys = set(genre_schema.fields.keys())
        schema_keys.remove('id')
        data_keys = request_data.keys()
        if 'id' in data_keys:
            data_keys = set(data_keys.remove('id'))
        else:
            data_keys = set(data_keys)
        if data_keys != schema_keys:
            return "Not all keys acquired", 400

        try:
            result_data = genre_service.update(genre_id, request_data)
        except NoResultFound:
            return f"Genre ID: {genre_id} not found", 404

        result = genre_schema.dump(result_data)
        return result, 200

    def patch(self, genre_id: int):

        request_data = request.json
        try:
            request_data = genre_schema.load(request_data)
        except ValidationError as err:
            return f"{err}", 400

        try:
            result_data = genre_service.update(genre_id, request_data)
        except NoResultFound:
            return f"Genre ID: {genre_id} not found", 404

        result = genre_schema.dump(result_data)
        return result, 200

    def delete(self, genre_id: int):

        try:
            genre_service.delete(genre_id)
        except NoResultFound:
            return f"Genre ID: {genre_id} not found", 404

        return f"Data ID: {genre_id} was deleted successfully.", 200
