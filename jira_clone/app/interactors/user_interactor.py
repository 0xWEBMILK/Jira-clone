from ..schemas import UserSchema


class UserInteractor:
    def __init__(self, repository, hasher):
        self.repository = repository
        self.hasher = hasher

    def get_user_by_token(self, token):
        return self.repository.get_user_by_token(token)

    def get_all_users(self):
        users = self.repository.get_all_users()

        return None if len(users) == 0 else users

    def create_user(self, user_schema: UserSchema):
        token = self.hasher.encode(user_schema)

        if self.get_user_by_token(token) is None:
            self.repository.create_user(token)

        return token

    def remove_user(self, user_schema: UserSchema):
        token = self.hasher.encode(user_schema)

        if self.get_user_by_token(token):
            self.repository.remove_user(token)

            return token

        return None

    def update_user(self, old_user_schema: UserSchema, new_user_schema: UserSchema):
        old_token = self.hasher.encode(old_user_schema)
        new_token = self.hasher.encode(new_user_schema)

        if self.get_user_by_token(old_token):
            self.repository.update_user(old_token, new_token)

            return new_token

        return None