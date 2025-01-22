from sqlalchemy.orm import Session
from typing import List, Type

from .base_repository import BaseRepository
from ..models import UserModel, BaseModel


class UserRepository(BaseRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, token: str) -> None:
        user = UserModel(token=token)
        self.session.add(user)
        self.session.commit()

    def remove(self, token: str) -> None:
        user = self.get_by_token(token)
        self.session.delete(user)
        self.session.commit()

    def update(self, old_token: str, new_token: str) -> None:
        user = self.get_by_token(old_token)
        user.token = new_token
        self.session.commit()

    def get_by_token(self, token: str) -> BaseModel | None:
        return self.session.query(UserModel).filter_by(token=token).first()

    def get_all(self) -> List[Type[BaseModel]]:
        return self.session.query(UserModel).all()