from typing import List

from ..schemas import CategorySchema

from .base_interactor import BaseInteractor
from ..models import BaseModel
from ..repositories import BaseRepository
from ..auth.hashing import BaseHasher


class CategoryInteractor(BaseInteractor):
    def __init__(self, repository: BaseRepository, hasher: BaseHasher):
        self.repository = repository
        self.hasher = hasher

    def get_by_token(self, token: str) -> BaseModel | None:
        return self.repository.get_by_token(token)

    def get_all(self) -> List[BaseModel]:
        categories = self.repository.get_all()

        return None if len(categories) == 0 else categories

    def create(self, category_schema: CategorySchema) -> str | None:
        token = self.hasher.encode(category_schema)

        if self.get_by_token(token) is None:
            self.repository.create(token)

        return token

    def remove(self, category_schema: CategorySchema) -> str | None:
        token = self.hasher.encode(category_schema)

        if self.get_by_token(token):
            self.repository.remove(token)

            return token

        return None

    def update(self, old_schema: CategorySchema, new_schema: CategorySchema) -> str | None:
        old_token = self.hasher.encode(old_schema)
        new_token = self.hasher.encode(new_schema)

        if self.get_by_token(old_token):
            self.repository.update(old_token, new_token)

            return new_token

        return None