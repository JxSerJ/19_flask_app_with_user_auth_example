import jwt
from helpers.constants import SECRET, JWT_ALGORITHM
from flask import request, abort


def auth_required(func):
    def wrapper(*args, **kwargs):

        if "Authorization" not in request.headers:
            abort(401)

        auth_data = request.headers["Authorization"]
        token = auth_data.split("Bearer ")[-1]

        try:
            user_data = jwt.decode(token, SECRET, algorithms=JWT_ALGORITHM)
        except Exception as err:
            print("JWT Decode Exception: ", err)
            abort(401)

        print(f'User: {user_data["username"]}. Role: {user_data["role"]}. Authorized.')

        return func(*args, **kwargs)

    return wrapper


def admin_required(func):
    def wrapper(*args, **kwargs):

        if "Authorization" not in request.headers:
            abort(401)

        auth_data = request.headers["Authorization"]
        token = auth_data.split("Bearer ")[-1]
        role = None

        try:
            decoded_data = jwt.decode(token, SECRET, algorithms=JWT_ALGORITHM)
            role = decoded_data.get("role", "user")
        except Exception as err:
            print("JWT Decode Exception: ", err)
            abort(401)

        if role != "admin":
            abort(403)

        return func(*args, **kwargs)

    return wrapper
