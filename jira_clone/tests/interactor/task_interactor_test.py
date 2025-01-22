from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from jira_clone.app.database.database import Base
from jira_clone.app.repositories.task_repository import TaskRepository
from jira_clone.app.interactors.task_interactor import TaskInteractor

from jira_clone.app.schemas.schemas import TaskSchema
from jira_clone.app.auth.hashing import JWTHasher

jwt_hasher = JWTHasher('super', 'HS256')

engine = create_engine('sqlite:///test.db')
session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

def get_session():
    with session() as conn:
        try:
            return conn
        except Exception as e:
            conn.rollback()
            raise e

def test_create_task():
    task_repository = TaskRepository(get_session())
    task_interactor = TaskInteractor(task_repository, jwt_hasher)

    task_schema = TaskSchema(
        title='Test Task',
        description='Test Task Description',

        performers=['Some guy'],
        tags=['Some tag'],
        creator='Some guy',
    )

    token = task_interactor.create_task(task_schema)

    assert task_interactor.get_task_by_token(token) is not None

def test_remove_task():
    task_repository = TaskRepository(get_session())
    task_interactor = TaskInteractor(task_repository, jwt_hasher)

    task_schema = TaskSchema(
        title='Test Task',
        description='Test Task Description',

        performers=['Some guy'],
        tags=['Some tag'],
        creator='Some guy',
    )

    token = task_interactor.remove_task(task_schema)

    assert task_interactor.get_task_by_token(token) is None

def test_update_task():
    task_repository = TaskRepository(get_session())
    task_interactor = TaskInteractor(task_repository, jwt_hasher)

    old_task_schema = TaskSchema(
        title='Test Task',
        description='Test Task Description',

        performers=['Some guy'],
        tags=['Some tag'],
        creator='Some guy',
    )

    new_task_schema = TaskSchema(
        title='Test Task123',
        description='Test Task Description123',

        performers=['Some guy'],
        tags=['Some tag'],
        creator='Some guy',
    )

    task_interactor.create_task(old_task_schema)
    token = task_interactor.update_task(old_task_schema, new_task_schema)

    assert token is not None