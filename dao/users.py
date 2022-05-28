from dao.model.users import User


# CRUD
class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_all(self):

        result_data = self.session.query(User).all()
        return result_data

    def get_one(self, user_id: int):

        result_data = self.session.query(User).filter(User.id == user_id).one()
        return result_data

    def get_by_username(self, username: str):

        result_data = self.session.query(User).filter(User.username == username).one()
        return result_data

    def create(self, data):

        new_user = User(**data)

        self.session.add(new_user)
        self.session.commit()
        return new_user

    def update(self, user, data):

        for k, v in data.items():
            setattr(user, k, v)
        self.session.add(user)
        self.session.commit()
        return user

    def delete(self, user_id: int):

        user = self.get_one(user_id)
        self.session.delete(user)
        self.session.commit()
