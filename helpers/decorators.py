import calendar
import datetime

import jwt
from helpers.constants import SECRET, JWT_ALGORITHM
from flask import request, abort
from container import user_service


def auth_required(func):
    def wrapper(*args, **kwargs):

        if "Authorization" not in request.headers:
            abort(401)

        auth_data = request.headers["Authorization"]
        token = auth_data.split("Bearer ")[-1]

        try:
            user_data = jwt.decode(token, SECRET, algorithms=JWT_ALGORITHM)
            user = user_service.get_by_username(user_data.get('username', None))  # check if user exists in user db
            if user is None:
                abort(404, 'User name and password are incorrect')
            if user_data.get("expiration") < calendar.timegm(datetime.datetime.utcnow().timetuple()):
                raise Exception('Token expired.')
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
            user = user_service.get_by_username(decoded_data.get('username', None))  # check if user exists in user db
            if user is None:
                abort(404, "User doesn't exists")
            if decoded_data.get("expiration") < calendar.timegm(datetime.datetime.utcnow().timetuple()):
                raise Exception('Token expired.')
        except Exception as err:
            print("JWT Decode Exception: ", err)
            abort(401, str(err))

        if role != "admin":
            abort(403)

        return func(*args, **kwargs)

    return wrapper
