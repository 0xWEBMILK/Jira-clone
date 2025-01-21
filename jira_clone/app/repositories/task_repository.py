from sqlalchemy.orm import Session
from ..models import TaskModel

class TaskRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_task(self, token: str):
        new_task = TaskModel(token=token)
        self.session.add(new_task)
        self.session.commit()

    def remove_task(self, token: str):
        task = self.get_task_by_token(token)
        self.session.delete(task)
        self.session.commit()

    def update_task(self, old_token: str, new_token: str):
        task = self.get_task_by_token(old_token)
        task.token = new_token
        self.session.commit()

    def get_task_by_token(self, token: str):
        return self.session.query(TaskModel).filter_by(token=token).first()

    def get_all_tasks(self):
        return self.session.query(TaskModel).all()