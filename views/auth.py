from flask import request
from flask_restx import Resource
from container import auth_service


class AuthsView(Resource):
    def post(self):
        data = request.json

        username = data.get("username", None)
        password = data.get("password", None)

        if None in [username, password]:
            return '', 400

        tokens = auth_service.generate_tokens(username, password)
        return tokens, 201
