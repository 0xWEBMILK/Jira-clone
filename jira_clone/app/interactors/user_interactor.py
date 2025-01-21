from ..schemas import UserSchema


class UserInteractor:
    def __init__(self, repository, hasher):
        self.repository = repository
        self.hasher = hasher

    def get_all_users(self) -> list[str]:
        users = list(map(lambda x: x.token, self.repository.get_all_users()))

        return users

    def get_user_by_token(self, user_token: str):
        encoded = self.repository.get_user_by_token(user_token)

        if encoded is not None:
            user = self.hasher.decode(encoded.token)

            return user

        return 404

    def create_user(self, user_schema: UserSchema):
        token = self.hasher.encode(user_schema)

        if self.repository.get_user_by_token(token):
            self.repository.create_user(token)

            return token

        return 404

    def remove_user(self, user_schema: UserSchema):
        token = self.hasher.encode(user_schema)

        if self.repository.get_user_by_token(token):
            self.repository.remove_user(token)

            return token

        return 404

    def update_user(self, old_user_schema: UserSchema, new_user_schema: UserSchema):
        old_token = self.hasher.encode(old_user_schema)
        new_token = self.hasher.encode(new_user_schema)

        if self.repository.get_user_by_token(old_token):
            self.repository.update_user(old_token, new_token)

            return new_token

        return 404