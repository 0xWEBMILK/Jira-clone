import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from jira_clone.app.database.database import Base
from jira_clone.app.repositories.task_repository import TaskRepository
from jira_clone.app.schemas.schemas import TaskSchema
from jira_clone.app.auth.hashing import JWTHasher

jwt_hasher = JWTHasher('super', 'HS256')
DATABASE_URL = 'sqlite:///test.db'

@pytest.fixture(scope='function')
def session():
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    session = Session()

    yield session

    session.close()
    Base.metadata.drop_all(engine)

@pytest.fixture
def task_schema():
    return TaskSchema(
        title="Some test task",
        description="Some test task description",
        creator="some_creator",
        performers=["some_performer"],
        tags=["some_tag"],
    )

def test_create(session, task_schema):
    token = jwt_hasher.encode(task_schema)
    task_repository = TaskRepository(session)
    task_repository.create(token)

    assert task_repository.get_by_token(token).token

def test_remove(session, task_schema):
    token = jwt_hasher.encode(task_schema)
    task_repository = TaskRepository(session)
    task_repository.create(token)

    task_repository.remove(token)

    assert task_repository.get_by_token(token) is None

def test_update(session, task_schema):
    old_token = jwt_hasher.encode(task_schema)
    task_repository = TaskRepository(session)
    task_repository.create(old_token)

    updated_schema = TaskSchema(
        title="Some test task123",
        description="Some test task description132",
        creator="some_creator",
        performers=["some_performer"],
        tags=["some_tag"],
    )
    new_token = jwt_hasher.encode(updated_schema)

    task_repository.update(old_token, new_token)

    assert task_repository.get_by_token(new_token).token == new_token
