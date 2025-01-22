from sqlalchemy.orm import Session
from typing import List, Type

from .base_repository import BaseRepository
from ..models import TagModel, BaseModel


class TagRepository(BaseRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, token: str) -> None:
        tag = TagModel(token=token)
        self.session.add(tag)
        self.session.commit()

    def remove(self, token: str) -> None:
        tag = self.get_by_token(token)
        self.session.delete(tag)
        self.session.commit()

    def update(self, old_token: str, new_token: str) -> None:
        tag = self.get_by_token(old_token)
        tag.token = new_token
        self.session.commit()

    def get_by_token(self, token: str) -> BaseModel | None:
        return self.session.query(TagModel).filter_by(token=token).first()

    def get_all(self) -> List[Type[BaseModel]]:
        return self.session.query(TagModel).all()