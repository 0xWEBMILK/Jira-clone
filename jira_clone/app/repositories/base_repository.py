from abc import ABC, abstractmethod
from typing import Type

from ..models import BaseModel


class BaseRepository(ABC):
    @abstractmethod
    def create(self, token: str) -> None:
        pass

    @abstractmethod
    def remove(self, token: str) -> None:
        pass

    @abstractmethod
    def update(self, old_token: str, new_token: str) -> None:
        pass

    @abstractmethod
    def get_by_token(self, token: str) -> BaseModel | None:
        pass

    @abstractmethod
    def get_all(self) -> list[BaseModel]:
        pass