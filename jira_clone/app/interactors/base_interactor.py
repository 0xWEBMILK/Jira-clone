from abc import ABC, abstractmethod
from typing import List

from ..models import BaseModel

class BaseInteractor(ABC):
    @abstractmethod
    def create(self, schema) -> str:
        pass

    @abstractmethod
    def remove(self, schema) -> str | None:
        pass

    @abstractmethod
    def update(self, old_schema, new_schema) -> str | None:
        pass

    @abstractmethod
    def get_by_token(self, token: str) -> str | None:
        pass

    @abstractmethod
    def get_all(self) -> List[BaseModel] | None:
        pass