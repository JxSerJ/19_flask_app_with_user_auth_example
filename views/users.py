from flask import request, jsonify
from flask_restx import Resource, Namespace

from helpers.decorators import admin_required
from views.validator import validator
from marshmallow import ValidationError
from sqlalchemy.exc import NoResultFound

from container import user_service
from dao.model.users import UserSchema, User

users_ns = Namespace('users')

user_schema = UserSchema()
users_schema = UserSchema(many=True)


@users_ns.route('/')
class UsersView(Resource):

    @admin_required
    def get(self):

        result_data = user_service.get_all()
        if len(result_data) == 0:
            return "Data not found. Empty database.", 404

        result = users_schema.dump(result_data)
        return result, 200

    @admin_required
    def post(self):

        request_data = request.json
        try:
            validator("POST", request_data, User, user_schema)
        except ValidationError as err:
            return err.messages, 400

        result_data = user_service.create(request_data)

        result = user_schema.dump(result_data)

        data_id = result["id"]

        response = jsonify(result)
        response.status_code = 201
        response.headers['location'] = f'/{users_ns.name}/{data_id}'

        return response


@users_ns.route('/<int:user_id>')
class UserView(Resource):
    @admin_required
    def get(self, user_id: int):

        try:
            result_data = user_service.get_one(user_id)
        except NoResultFound:
            return f"User ID: {user_id} not found", 404

        result = user_schema.dump(result_data)
        return result, 200

    @admin_required
    def put(self, user_id: int):

        request_data = request.json
        try:
            request_data = user_schema.load(request_data)
        except ValidationError as err:
            return f"{err}", 400

        # check if all keys acquired
        schema_keys = set(user_schema.fields.keys())
        schema_keys.remove('id')
        data_keys = request_data.keys()
        if 'id' in data_keys:
            data_keys = set(data_keys.remove('id'))
        else:
            data_keys = set(data_keys)
        if data_keys != schema_keys:
            return "Not all keys acquired", 400

        try:
            result_data = user_service.update(user_id, request_data)
        except NoResultFound:
            return f"User ID: {user_id} not found", 404

        result = user_schema.dump(result_data)
        return result, 200

    @admin_required
    def patch(self, user_id: int):

        request_data = request.json
        try:
            request_data = user_schema.load(request_data)
        except ValidationError as err:
            return f"{err}", 400

        try:
            result_data = user_service.update(user_id, request_data)
        except NoResultFound:
            return f"User ID: {user_id} not found", 404

        result = user_schema.dump(result_data)
        return result, 200

    @admin_required
    def delete(self, user_id: int):

        try:
            user_service.delete(user_id)
        except NoResultFound:
            return f"User ID: {user_id} not found", 404

        return f"Data ID: {user_id} was deleted successfully.", 200
