from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from jira_clone.app.database.database import Base
from jira_clone.app.repositories.task_repository import TaskRepository
from jira_clone.app.schemas.schemas import TaskSchema

from jira_clone.app.auth.hashing import HasherInterface, JWTHasher

jwt_hasher = JWTHasher('super', 'HS256')
jwt_hasher_interface = HasherInterface(jwt_hasher)

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
    test_task_schema = TaskSchema(
        title="Some test task",
        description="Some test task description",
        
        creator="some_creator",
        performers=["some_performer"],
        tags=["some_tag"],
    )

    token = jwt_hasher_interface.encode(test_task_schema)
    task_repository = TaskRepository(get_session())
    task_repository.create_task(token)

    assert task_repository.get_task_by_token(token).token

def test_remove_task():
    test_task_schema = TaskSchema(
        title="Some test task",
        description="Some test task description",

        creator="some_creator",
        performers=["some_performer"],
        tags=["some_tag"],
    )

    token = jwt_hasher_interface.encode(test_task_schema)
    task_repository = TaskRepository(get_session())
    task_repository.remove_task(token)

    assert task_repository.get_task_by_token(token) is None

def test_update_task():
    test_task_schema = TaskSchema(
        title="Some test task",
        description="Some test task description",

        creator="some_creator",
        performers=["some_performer"],
        tags=["some_tag"],
    )

    old_token = jwt_hasher_interface.encode(test_task_schema)
    task_repository = TaskRepository(get_session())

    task_repository.create_task(old_token)

    test_task_schema = TaskSchema(
        title="Some test task123",
        description="Some test task description132",

        creator="some_creator",
        performers=["some_performer"],
        tags=["some_tag"],
    )

    new_token = jwt_hasher_interface.encode(test_task_schema)

    task_repository.update_task(old_token, new_token)

    assert task_repository.get_task_by_token(new_token).token == new_token
