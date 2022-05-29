import base64
import hmac
from hashlib import pbkdf2_hmac

from helpers.constants import PWD_HASH_ALGORITHM, PWD_HASH_SALT, PWD_HASH_ITERATIONS
from dao.users import UserDAO


class UserService:
    def __init__(self, dao: UserDAO):
        self.user_dao = dao

    def get_all(self):
        result_data = self.user_dao.get_all()
        return result_data

    def get_one(self, user_id: int):
        result_data = self.user_dao.get_one(user_id)
        return result_data

    def get_by_username(self, username):
        result_data = self.user_dao.get_by_username(username)
        return result_data

    def generate_pwd_hash(self, password: str) -> bytes:
        hash_digest = pbkdf2_hmac(
            PWD_HASH_ALGORITHM,
            password.encode('utf-8'),  # encode into bytes
            PWD_HASH_SALT.encode('utf-8'),
            PWD_HASH_ITERATIONS
        )
        return hash_digest

    def generate_pwd_hash_b64(self, password: str) -> bytes:
        hash_digest = self.generate_pwd_hash(password)
        result_data = base64.b64encode(hash_digest)
        return result_data

    def compare_passwords(self, password_hash, password_for_comparison) -> bool:
        pwd_hash_decoded_digest = base64.b64decode(password_hash)
        pwd_for_comp_hash_digest = self.generate_pwd_hash(password_for_comparison)

        result = hmac.compare_digest(pwd_hash_decoded_digest, pwd_for_comp_hash_digest)

        return result

    def create(self, data):
        data['password'] = self.generate_pwd_hash(data['password'])
        result_data = self.user_dao.create(data)
        return result_data

    def update(self, user_id: int, data):
        user = self.user_dao.get_one(user_id)
        result_data = self.user_dao.update(user, data)
        return result_data

    def delete(self, user_id: int):
        query = self.user_dao.get_one(user_id)
        self.user_dao.delete(user_id)
