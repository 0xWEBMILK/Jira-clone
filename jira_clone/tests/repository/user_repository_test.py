from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from jira_clone.app.database.database import Base
from jira_clone.app.repositories.user_repository import UserRepository
from jira_clone.app.schemas.schemas import UserSchema

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


def test_create_user():
    test_user_schema = UserSchema(
        first_name="some",
        last_name="user",

        username="some_username",
        password="some_password",
        email="someemail@email.com",
    )

    token = jwt_hasher_interface.encode(test_user_schema)
    user_repository = UserRepository(get_session())
    user_repository.create_user(token)

    assert user_repository.get_user_by_token(token).token


def test_remove_user():
    test_user_schema = UserSchema(
        first_name="some",
        last_name="user",

        username="some_username",
        password="some_password",
        email="someemail@email.com",
    )

    token = jwt_hasher_interface.encode(test_user_schema)
    user_repository = UserRepository(get_session())
    user_repository.remove_user(token)

    assert user_repository.get_user_by_token(token) is None


def test_update_user():
    test_user_schema = UserSchema(
        first_name="some",
        last_name="user",

        username="some_username",
        password="some_password",
        email="someemail@email.com",
    )

    old_token = jwt_hasher_interface.encode(test_user_schema)
    user_repository = UserRepository(get_session())

    user_repository.create_user(old_token)

    test_user_schema = UserSchema(
        first_name="some",
        last_name="user",

        username="some_username",
        password="some_password123",
        email="someemail@email.com",
    )

    new_token = jwt_hasher_interface.encode(test_user_schema)

    user_repository.update_user(old_token, new_token)

    assert user_repository.get_user_by_token(new_token).token == new_token
