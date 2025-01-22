from typing import Type, List

from sqlalchemy.orm import Session

from .base_repository import BaseRepository
from ..models import CategoryModel, BaseModel


class CategoryRepository(BaseRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, token: str) -> None:
        new_category = CategoryModel(token=token)
        self.session.add(new_category)
        self.session.commit()

    def remove(self, token: str) -> None:
        category = self.get_by_token(token)
        self.session.delete(category)
        self.session.commit()

    def update(self, old_token: str, new_token: str) -> None:
        category = self.get_by_token(old_token)
        category.token = new_token
        self.session.commit()

    def get_by_token(self, token: str) -> BaseModel | None:
        return self.session.query(CategoryModel).filter_by(token=token).first()

    def get_all(self) -> List[Type[BaseModel]]:
        return self.session.query(CategoryModel).all()