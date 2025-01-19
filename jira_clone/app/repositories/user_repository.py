class UserRepository:
    def __init__(self, session):
        self.session = session

    def add_user(self, token: str):
        self.session.add('users', token)

    def remove_user(self, token: str):
        self.session.remove('users', token)

    def update_user(self, old_token: str, new_token: str):
        if self.get_user_by_token(old_token):
            self.session.update('users', old_token, new_token)

    def get_user_by_token(self, token: str):
        for item in self.session.all()['users']:
            if item == token:
                return item