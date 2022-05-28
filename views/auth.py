from flask import request
from flask_restx import Resource


class AuthsView(Resource):
    def post(self):
        data = request.json

        username = data.get("username", None)
        password = data.get("password", None)

        if None in [username, password]:
            return '', 400

        tokens = None
        return tokens, 201
