from jira_clone.app.models.models import User

from datetime import datetime, timedelta, UTC
from jose import jwt


class HasherInterface:
    def __init__(self, hasher):
        self.hasher = hasher

    def encode(self, user: User) -> str:
        return self.hasher.encode(user)

    def decode(self, token) -> str:
        return self.hasher.decode(token)


class JWTHasher:
    def __init__(self, key, alg = 'HS256'):
        self.key = key
        self.alg = alg

    def encode(self, user: User):
        to_encode = user.model_dump()
        expire_date = datetime.now(UTC) + timedelta(minutes=30)

        to_encode['exp'] = expire_date

        encoded = jwt.encode(to_encode, self.key, self.alg)
        return encoded

    def decode(self, token):
        decoded = jwt.decode(token, self.key, self.alg)

        return User(**decoded)
