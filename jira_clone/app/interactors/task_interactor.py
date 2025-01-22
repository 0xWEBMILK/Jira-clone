from typing import List

from ..schemas import TaskSchema

from .base_interactor import BaseInteractor
from ..models import BaseModel
from ..repositories import BaseRepository
from ..auth.hashing import BaseHasher

class TaskInteractor(BaseInteractor):
    def __init__(self, repository: BaseRepository, hasher: BaseHasher):
        self.repository = repository
        self.hasher = hasher

    def get_by_token(self, token: str) -> BaseModel | None:
        return self.repository.get_by_token(token)

    def get_all(self) -> List[BaseModel] | None:
        tasks = self.repository.get_all()

        return None if len(tasks) == 0 else tasks

    def create(self, task_schema: TaskSchema):
        token = self.hasher.encode(task_schema)

        if self.get_by_token(token) is None:
            self.repository.create(token)

        return token

    def remove(self, task_schema: TaskSchema):
        token = self.hasher.encode(task_schema)

        if self.get_by_token(token):
            self.repository.remove(token)

            return token

        return None

    def update(self, old_schema: TaskSchema, new_schema: TaskSchema):
        old_token = self.hasher.encode(old_schema)
        new_token = self.hasher.encode(new_schema)

        if self.get_by_token(old_token):
            self.repository.update(old_token, new_token)

            return new_token

        return None