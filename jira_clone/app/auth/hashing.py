from jose import jwt

def get_hasher_stub():
    pass

class JWTHasher:
    def __init__(self, key, alg = 'HS256'):
        self.key = key
        self.alg = alg

    def encode(self, value):
        to_encode = value.model_dump()

        encoded = jwt.encode(to_encode, self.key, self.alg)
        return encoded

    def decode(self, token):
        decoded = jwt.decode(token, self.key, self.alg)

        return decoded
