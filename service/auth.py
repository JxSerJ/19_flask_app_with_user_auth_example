import calendar
import datetime

import jwt
from flask import abort

from helpers.constants import SECRET, JWT_ALGORITHM
from service.users import UserService

class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def generate_tokens(self, username, password):
        user = self.user_service.get_by_username(username)

        if user is None:
            abort(404)

        if not self.user_service.compare_passwords(user.password, password):
            abort(400)

        data = {
            "username": user.username,
            "role": user.role
        }

        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data["expiration"] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, SECRET, algorithm=JWT_ALGORITHM)

        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data["expiration"] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, SECRET, algorithm=JWT_ALGORITHM)

        tokens = {
            "access_token": access_token,
            "refresh_token": refresh_token
        }

        return tokens
