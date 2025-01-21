from ..schemas import TaskSchema


class TaskInteractor:
    def __init__(self, repository, hasher):
        self.repository = repository
        self.hasher = hasher

    def get_all_tasks(self) -> list[str]:
        tasks = list(map(lambda x: x.token, self.repository.get_all_tasks()))

        return tasks

    def get_task_by_token(self, task_token: str):
        encoded = self.repository.get_task_by_token(task_token)

        if encoded is not None:
            task = self.hasher.decode(encoded.token)

            return task

    def create_task(self, task_schema: TaskSchema):
        token = self.hasher.encode(task_schema)

        self.repository.create_task(token)

        return token

    def remove_task(self, task_schema: TaskSchema):
        token = self.hasher.encode(task_schema)

        self.repository.remove_task(token)

        return token

    def update_task(self, old_task_schema: TaskSchema, new_task_schema: TaskSchema):
        old_token = self.hasher.encode(old_task_schema)
        new_token = self.hasher.encode(new_task_schema)

        self.repository.update_task(old_token, new_token)

        return new_token