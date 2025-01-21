from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from jira_clone.app.database.database import Base
from jira_clone.app.repositories.tag_repository import TagRepository
from jira_clone.app.schemas.schemas import CategorySchema, ColorsEnum

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


def test_create_tag():
    test_tag_schema = CategorySchema(
        name="Some test tag",
        color=ColorsEnum.RED
    )

    token = jwt_hasher_interface.encode(test_tag_schema)
    tag_repository = TagRepository(get_session())
    tag_repository.create_tag(token)

    assert tag_repository.get_tag_by_token(token).token

def test_remove_tag():
    test_tag_schema = CategorySchema(
        name="Some test tag",
        color=ColorsEnum.RED
    )

    token = jwt_hasher_interface.encode(test_tag_schema)
    tag_repository = TagRepository(get_session())
    tag_repository.remove_tag(token)

    assert tag_repository.get_tag_by_token(token) is None

def test_update_tag():
    test_tag_schema = CategorySchema(
        name="Some test tag",
        color=ColorsEnum.RED
    )

    old_token = jwt_hasher_interface.encode(test_tag_schema)
    tag_repository = TagRepository(get_session())

    tag_repository.create_tag(old_token)

    test_tag_schema = CategorySchema(
        name="Some test tag123",
        color=ColorsEnum.RED
    )

    new_token = jwt_hasher_interface.encode(test_tag_schema)

    tag_repository.update_tag(old_token, new_token)

    assert tag_repository.get_tag_by_token(new_token).token == new_token
