from sqlalchemy.orm import Session
from ..models import UserModel

class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_user(self, token: str):
        new_user = UserModel(token=token)
        self.session.add(new_user)
        self.session.commit()

    def remove_user(self, token: str):
        user = self.get_user_by_token(token)
        self.session.delete(user)
        self.session.commit()

    def update_user(self, old_token: str, new_token: str):
        user = self.get_user_by_token(old_token)
        user.token = new_token
        self.session.commit()

    def get_user_by_token(self, token: str):
        return self.session.query(UserModel).filter_by(token=token).first()

    def get_all_users(self):
        return self.session.query(UserModel).all()