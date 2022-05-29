from flask import request, jsonify
from flask_restx import Resource, Namespace

from helpers.decorators import admin_required
from views.validator import validator
from marshmallow import ValidationError
from sqlalchemy.exc import NoResultFound

from container import user_service, auth_service
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
        for entry in result:
            entry['password'] = entry['password'].decode('utf-8')
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
        user_token_entry_id = auth_service.create_token_entry_in_db(data_id).id
        result['token_id'] = user_token_entry_id
        user_service.update(data_id, {'token_id': user_token_entry_id})

        return f"User created. User ID:{data_id}", 201, {'location': f'/{users_ns.name}/{data_id}'}


@users_ns.route('/<int:user_id>')
class UserView(Resource):
    @admin_required
    def get(self, user_id: int):

        try:
            result_data = user_service.get_one(user_id)
        except NoResultFound:
            return f"User ID: {user_id} not found", 404

        result = user_schema.dump(result_data)
        result['password'] = result['password'].decode('utf-8')
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
        result['password'] = result['password'].decode('utf-8')
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
        result['password'] = result['password'].decode('utf-8')
        return result, 200

    @admin_required
    def delete(self, user_id: int):

        try:
            user_service.delete(user_id)
        except NoResultFound:
            return f"User ID: {user_id} not found", 404

        auth_service.delete(user_id)

        return f"Data ID: {user_id} was deleted successfully.", 200
