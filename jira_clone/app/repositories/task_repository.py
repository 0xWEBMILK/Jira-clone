class TaskRepository:
    def __init__(self, session):
        self.session = session

    def create_task(self, token: str):
        self.session.add('tasks', token)

    def remove_task(self, token: str):
        self.session.remove('tasks', token)

    def is_task_exist(self, token: str):
        for item in self.session.all()['tokens']:
            if item == token:
                return token