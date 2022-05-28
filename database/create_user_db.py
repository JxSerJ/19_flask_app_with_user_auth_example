import base64
import json
from hashlib import pbkdf2_hmac

from flask import current_app

from dao.model.tokens import Token
from helpers.constants import INITIAL_DATA_PATH, PWD_HASH_ALGORITHM, PWD_HASH_SALT, PWD_HASH_ITERATIONS
from dao.model.users import User


def create_user_data(db):
    try:
        with current_app.app_context():
            db.drop_all(bind='tokens')
            db.create_all(bind='tokens')
            print('\nAll access tokens has been removed.\n')
            print("Generating user database...")
            if current_app.config['DEBUG']:
                print('Debug mode detected. User database will be regenerated with plain-view passwords.')
            db.drop_all(bind='users')
            db.create_all(bind='users')

            with open(INITIAL_DATA_PATH, 'r', encoding='UTF-8') as file:
                file_data = json.load(file)

            new_users = []
            tokens = []
            print('Generating hashes for passwords of known users. Hang tight. It can take a while. Hash algorithms '
                  'are strong here...\n')
            for entry in file_data['users']:
                print(f'Generating hash for user {entry["username"]}')
                entry['password_in_plain_view'] = entry['password']
                hash_digest = pbkdf2_hmac(
                    PWD_HASH_ALGORITHM,
                    entry['password'].encode('utf-8'),  # encode into bytes
                    PWD_HASH_SALT.encode('utf-8'),
                    PWD_HASH_ITERATIONS
                )
                entry['password'] = base64.b64encode(hash_digest)
                if not current_app.config['DEBUG']:
                    entry.pop('password_in_plain_view')
                new_user = User(**entry)
                new_users.append(new_user)
            print('\nHash generation complete.')

            db.session.add_all(new_users)
            db.session.commit()

            print("Generating null-tokens...")
            for user in new_users:
                token = Token(user_id=user.id)
                tokens.append(token)
            db.session.add_all(tokens)
            db.session.commit()

            updated_users = []
            for user in new_users:
                for token in tokens:
                    if token.user_id == user.id:
                        user.token_id = token.id
                        updated_users.append(user)
            db.session.add_all(updated_users)
            db.session.commit()
            print("Null-tokens generated.")
            db.session.close()

        print("User database regenerated successfully!\n")

    except Exception as err:
        print(f"User database error: {err}\n"
              f"User database regeneration incomplete. Data may be corrupted!\n")
