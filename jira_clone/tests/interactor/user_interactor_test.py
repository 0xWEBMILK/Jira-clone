import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from jira_clone.app.database.database import Base
from jira_clone.app.repositories.user_repository import UserRepository
from jira_clone.app.interactors.user_interactor import UserInteractor
from jira_clone.app.schemas.schemas import UserSchema
from jira_clone.app.auth.hashing import JWTHasher

jwt_hasher = JWTHasher('super', 'HS256')
DATABASE_URL = "sqlite:///test.db"

@pytest.fixture(scope='function')
def session():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)

def test_create_user(session):
    user_repository = UserRepository(session)
    user_interactor = UserInteractor(user_repository, jwt_hasher)

    user_schema = UserSchema(
        first_name='Test',
        last_name='User',
        username='test_user',
        password='sometestpassword',
        email='testemail@email.com'
    )

    token = user_interactor.create(user_schema)

    assert user_interactor.get_by_token(token) is not None

def test_remove_user(session):
    user_repository = UserRepository(session)
    user_interactor = UserInteractor(user_repository, jwt_hasher)

    user_schema = UserSchema(
        first_name='Test',
        last_name='User',
        username='test_user',
        password='sometestpassword',
        email='testemail@email.com'
    )

    token = user_interactor.remove(user_schema)

    assert user_interactor.get_by_token(token) is None

def test_update_user(session):
    user_repository = UserRepository(session)
    user_interactor = UserInteractor(user_repository, jwt_hasher)

    old_user_schema = UserSchema(
        first_name='Test',
        last_name='User',
        username='test_user',
        password='sometestpassword',
        email='testemail@email.com'
    )

    new_user_schema = UserSchema(
        first_name='Test123',
        last_name='User123',
        username='test_user',
        password='sometestpassword',
        email='testemail@email.com'
    )

    user_interactor.create(old_user_schema)
    token = user_interactor.update(old_user_schema, new_user_schema)

    assert token is not None
