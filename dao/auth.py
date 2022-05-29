from dao.model.auth import Token


# CRUD
class AuthDAO:
    def __init__(self, session):
        self.session = session

    def get_one_by_token_id(self, token_id):
        result_data = self.session.query(Token).get(token_id)
        return result_data

    def get_one_by_user_id(self, user_id: int):

        result_data = self.session.query(Token).filter(Token.user_id == user_id).one()
        return result_data

    def create(self, data):

        new_token = Token(**data)

        self.session.add(new_token)
        self.session.commit()
        return new_token

    def update(self, token, token_data):

        for k, v in token_data.items():
            setattr(token, k, v)
        self.session.add(token)
        self.session.commit()
        return token

    def delete(self, user_id: int):

        token = self.get_one_by_user_id(user_id)
        self.session.delete(token)
        self.session.commit()
