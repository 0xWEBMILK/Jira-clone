import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from jira_clone.app.models.base_model import Base
from jira_clone.app.repositories.user_repository import UserRepository
from jira_clone.app.schemas.schemas import UserSchema
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

def test_create(session):
    test_schema = UserSchema(
        first_name="some",
        last_name="user",
        username="somename",
        password="some_password",
        email="someemail@email.com",
    )

    token = jwt_hasher.encode(test_schema)
    user_repository = UserRepository(session)
    user_repository.create(token)

    assert user_repository.get_by_token(token).token

def test_remove(session):
    test_schema = UserSchema(
        first_name="some",
        last_name="user",
        username="somename",
        password="some_password",
        email="someemail@email.com",
    )

    token = jwt_hasher.encode(test_schema)
    user_repository = UserRepository(session)
    user_repository.create(token)

    user_repository.remove(token)

    assert user_repository.get_by_token(token) is None

def test_update(session):
    test_schema = UserSchema(
        first_name="some",
        last_name="user",
        username="somename",
        password="some_password",
        email="someemail@email.com",
    )

    old_token = jwt_hasher.encode(test_schema)
    user_repository = UserRepository(session)
    user_repository.create(old_token)

    test_schema = UserSchema(
        first_name="some",
        last_name="user",
        username="somename",
        password="some_password123",
        email="someemail@email.com",
    )

    new_token = jwt_hasher.encode(test_schema)

    user_repository.update(old_token, new_token)

    assert user_repository.get_by_token(new_token).token == new_token
