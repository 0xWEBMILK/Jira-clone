from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from jira_clone.app.database.database import Base
from jira_clone.app.repositories.user_repository import UserRepository
from jira_clone.app.interactors.user_interactor import UserInteractor

from jira_clone.app.schemas.schemas import UserSchema
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

def test_create_user():
    user_repository = UserRepository(get_session())
    user_interactor = UserInteractor(user_repository, jwt_hasher)

    user_schema = UserSchema(
        first_name='Test',
        last_name='User',

        username='test_user',
        password='sometestpassword',
        email='testemail@email.com'
    )

    token = user_interactor.create_user(user_schema)

    assert user_interactor.get_user_by_token(token) is not None

def test_remove_user():
    user_repository = UserRepository(get_session())
    user_interactor = UserInteractor(user_repository, jwt_hasher)

    user_schema = UserSchema(
        first_name='Test',
        last_name='User',

        username='test_user',
        password='sometestpassword',
        email='testemail@email.com'
    )

    token = user_interactor.remove_user(user_schema)

    assert user_interactor.get_user_by_token(token) is None

def test_update_user():
    user_repository = UserRepository(get_session())
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

    user_interactor.create_user(old_user_schema)
    token = user_interactor.update_user(old_user_schema, new_user_schema)

    assert token is not None