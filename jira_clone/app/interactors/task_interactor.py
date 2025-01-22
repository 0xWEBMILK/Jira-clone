from ..schemas import TaskSchema


class TaskInteractor:
    def __init__(self, repository, hasher):
        self.repository = repository
        self.hasher = hasher

    def get_task_by_token(self, token):
        return self.repository.get_task_by_token(token)

    def get_all_tasks(self):
        tasks = self.repository.get_all_tasks()

        return None if len(tasks) == 0 else tasks

    def create_task(self, task_schema: TaskSchema):
        token = self.hasher.encode(task_schema)

        if self.get_task_by_token(token) is None:
            self.repository.create_task(token)

        return token

    def remove_task(self, task_schema: TaskSchema):
        token = self.hasher.encode(task_schema)

        if self.get_task_by_token(token):
            self.repository.remove_task(token)

            return token

        return None

    def update_task(self, old_task_schema: TaskSchema, new_task_schema: TaskSchema):
        old_token = self.hasher.encode(old_task_schema)
        new_token = self.hasher.encode(new_task_schema)

        if self.get_task_by_token(old_token):
            self.repository.update_task(old_token, new_token)

            return new_token

        return None