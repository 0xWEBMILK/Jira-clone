from datetime import datetime, timedelta, UTC
from jose import jwt


class HasherInterface:
    def __init__(self, hasher):
        self.hasher = hasher

    def encode(self, value):
        return self.hasher.encode(value)

    def decode(self, token):
        return self.hasher.decode(token)


class JWTHasher:
    def __init__(self, key, alg = 'HS256'):
        self.key = key
        self.alg = alg

    def encode(self, value):
        to_encode = value.model_dump()
        expire_date = datetime.now(UTC) + timedelta(minutes=30)

        to_encode['exp'] = expire_date

        encoded = jwt.encode(to_encode, self.key, self.alg)
        return encoded

    def decode(self, token):
        decoded = jwt.decode(token, self.key, self.alg)

        return decoded
