from dao.model.auth import Token


# CRUD
class AuthDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, token_id: int):

        result_data = self.session.query(Token).filter(Token.id == token_id).one()
        return result_data

    def create(self, data):

        new_token = Token(**data)

        self.session.add(new_token)
        self.session.commit()
        return new_token

    def update(self, token, data):

        for k, v in data.items():
            setattr(token, k, v)
        self.session.add(token)
        self.session.commit()
        return token

    def delete(self, token_id: int):

        token = self.get_one(token_id)
        self.session.delete(token)
        self.session.commit()
