from sqlalchemy.orm import Session
from typing import List, Type

from .base_repository import BaseRepository
from ..models import TaskModel, BaseModel


class TaskRepository(BaseRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, token: str) -> None:
        task = TaskModel(token=token)
        self.session.add(task)
        self.session.commit()

    def remove(self, token: str) -> None:
        task = self.get_by_token(token)
        self.session.delete(task)
        self.session.commit()

    def update(self, old_token: str, new_token: str) -> None:
        task = self.get_by_token(old_token)
        task.token = new_token
        self.session.commit()

    def get_by_token(self, token: str) -> BaseModel | None:
        return self.session.query(TaskModel).filter_by(token=token).first()

    def get_all(self) -> List[Type[BaseModel]]:
        return self.session.query(TaskModel).all()