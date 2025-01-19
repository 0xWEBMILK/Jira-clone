class UserRepository:
    def __init__(self, session):
        self.session = session

    def add_user(self, token: str):
        self.session.add('users', token)

    def remove_user(self, token: str):
        self.session.remove('users', token)

    def is_user_exist(self, token: str):
        for item in self.session.all()['users']:
            if item == token:
                return item