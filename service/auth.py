import calendar
import datetime

import jwt
from flask import abort

from helpers.constants import SECRET, JWT_ALGORITHM
from service.users import UserService
from dao.auth import AuthDAO


class AuthService:
    def __init__(self, user_service: UserService, dao: AuthDAO):
        self.user_service = user_service
        self.auth_dao = dao

    def generate_tokens(self, username, password, is_refresh=False):
        user = self.user_service.get_by_username(username)

        if user is None:
            abort(404)

        if not is_refresh:
            print('User credentials acquired. Checking validity.')
            if not self.user_service.compare_passwords(user.password, password):
                abort(400)
            print(f'Credentials confirmed. User: {user.username}. Role: {user.role}. Generating tokens.')

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
        print(f'Tokens generated. Signature: {access_token[-8:]}/{refresh_token[-8:]}')

        return tokens

    def approve_refresh_token(self, refresh_token):

        print('Refresh token acquired. Checking validity.')

        data = jwt.decode(refresh_token, SECRET, algorithms=JWT_ALGORITHM)
        username = data.get('username')
        role = data.get('role')
        print(f'Credentials confirmed. User: {username}. Role: {role}. Generating tokens.')

        tokens = self.generate_tokens(username, None, is_refresh=True)

        return tokens
