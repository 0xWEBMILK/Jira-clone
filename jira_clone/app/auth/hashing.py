from jose import jwt
from abc import ABC, abstractmethod

def get_hasher_stub():
    pass

class BaseHasher(ABC):
    @abstractmethod
    def encode(self, value) -> str:
        pass

    @abstractmethod
    def decode(self, value) -> dict:
        pass

class JWTHasher(BaseHasher):
    def __init__(self, key, alg = 'HS256'):
        self.key = key
        self.alg = alg

    def encode(self, value) -> str:
        to_encode = value.model_dump()

        encoded = jwt.encode(to_encode, self.key, self.alg)
        return encoded

    def decode(self, token) -> dict:
        decoded = jwt.decode(token, self.key, self.alg)

        return decoded
