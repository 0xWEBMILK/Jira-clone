from jira_clone.app.models.models import UserModel
from sqlalchemy.orm import Session

class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_user(self, token: str):
        if self.get_user_by_token(token) is None:
            new_user = UserModel(token=token)
            self.session.add(new_user)
            self.session.commit()

    def remove_user(self, token: str):
        user = self.get_user_by_token(token)
        if user is not None:
            self.session.delete(user)
            self.session.commit()

    def update_user(self, old_token: str, new_token: str):
        user = self.get_user_by_token(old_token)
        if user:
            user.token = new_token
            self.session.commit()

    def get_user_by_token(self, token: str):
        return self.session.query(UserModel).filter_by(token=token).first()

    def get_all_users(self):
        return self.session.query(UserModel).all()