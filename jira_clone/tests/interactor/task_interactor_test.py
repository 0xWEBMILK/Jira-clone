import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from jira_clone.app.database.database import Base
from jira_clone.app.repositories.task_repository import TaskRepository
from jira_clone.app.interactors.task_interactor import TaskInteractor
from jira_clone.app.schemas.schemas import TaskSchema
from jira_clone.app.auth.hashing import JWTHasher
from jira_clone.app.config import get_config

config = get_config('../../')
jwt_hasher = JWTHasher('super', 'HS256')
DATABASE_URL = config.database.test_url

@pytest.fixture(scope='function')
def session():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)

def test_create_task(session):
    task_repository = TaskRepository(session)
    task_interactor = TaskInteractor(task_repository, jwt_hasher)

    task_schema = TaskSchema(
        title='Test Task',
        description='Test Task Description',
        performers=['Some guy'],
        category='Category 1',
        tags=['Some tag'],
        creator='Some guy',
    )

    token = task_interactor.create(task_schema)

    assert task_interactor.get_by_token(token) is not None

def test_remove_task(session):
    task_repository = TaskRepository(session)
    task_interactor = TaskInteractor(task_repository, jwt_hasher)

    task_schema = TaskSchema(
        title='Test Task',
        description='Test Task Description',
        performers=['Some guy'],
        category='Category 1',
        tags=['Some tag'],
        creator='Some guy',
    )

    token = task_interactor.remove(task_schema)

    assert task_interactor.get_by_token(token) is None

def test_update_task(session):
    task_repository = TaskRepository(session)
    task_interactor = TaskInteractor(task_repository, jwt_hasher)

    old_task_schema = TaskSchema(
        title='Test Task',
        description='Test Task Description',
        performers=['Some guy'],
        category='Category 1',
        tags=['Some tag'],
        creator='Some guy',
    )

    new_task_schema = TaskSchema(
        title='Test Task123',
        description='Test Task Description123',
        performers=['Some guy'],
        category='Category 2',
        tags=['Some tag'],
        creator='Some guy',
    )

    task_interactor.create(old_task_schema)
    token = task_interactor.update(old_task_schema, new_task_schema)

    assert token is not None
