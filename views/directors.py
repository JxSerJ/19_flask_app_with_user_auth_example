from flask import request, jsonify
from flask_restx import Resource, Namespace

from helpers.decorators import auth_required, admin_required
from views.validator import validator
from marshmallow import ValidationError
from sqlalchemy.exc import NoResultFound

from container import director_service
from dao.model.directors import DirectorSchema, Director

directors_ns = Namespace('directors')

director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)


@directors_ns.route('/')
class DirectorsView(Resource):

    @auth_required
    def get(self):

        result_data = director_service.get_all()
        if len(result_data) == 0:
            return "Data not found. Empty database.", 404

        result = directors_schema.dump(result_data)
        return result, 200

    @admin_required
    def post(self):

        request_data = request.json
        try:
            validator("POST", request_data, Director, director_schema)
        except ValidationError as err:
            return err.messages, 400

        result_data = director_service.create(request_data)

        result = director_schema.dump(result_data)

        data_id = result["id"]

        response = jsonify(result)
        response.status_code = 201
        response.headers['location'] = f'/{directors_ns.name}/{data_id}'

        return response


@directors_ns.route('/<int:director_id>')
class DirectorView(Resource):

    @auth_required
    def get(self, director_id: int):

        try:
            result_data = director_service.get_one(director_id)
        except NoResultFound:
            return f"Director ID: {director_id} not found", 404

        result = director_schema.dump(result_data)
        return result, 200

    @admin_required
    def put(self, director_id: int):

        request_data = request.json
        try:
            request_data = director_schema.load(request_data)
        except ValidationError as err:
            return f"{err}", 400

        # check if all keys acquired
        schema_keys = set(director_schema.fields.keys())
        schema_keys.remove('id')
        data_keys = request_data.keys()
        if 'id' in data_keys:
            data_keys = set(data_keys.remove('id'))
        else:
            data_keys = set(data_keys)
        if data_keys != schema_keys:
            return "Not all keys acquired", 400

        try:
            result_data = director_service.update(director_id, request_data)
        except NoResultFound:
            return f"Director ID: {director_id} not found", 404

        result = director_schema.dump(result_data)
        return result, 200

    @admin_required
    def patch(self, director_id: int):

        request_data = request.json
        try:
            request_data = director_schema.load(request_data)
        except ValidationError as err:
            return f"{err}", 400

        try:
            result_data = director_service.update(director_id, request_data)
        except NoResultFound:
            return f"Director ID: {director_id} not found", 404

        result = director_schema.dump(result_data)
        return result, 200

    @admin_required
    def delete(self, director_id: int):

        try:
            director_service.delete(director_id)
        except NoResultFound:
            return f"Director ID: {director_id} not found", 404

        return f"Data ID: {director_id} was deleted successfully.", 200
