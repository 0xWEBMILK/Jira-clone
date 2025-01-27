import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from jira_clone.app.database.database import Base
from jira_clone.app.repositories.tag_repository import TagRepository
from jira_clone.app.schemas.schemas import CategorySchema, ColorsEnum
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
    test_schema = CategorySchema(name="Some test tag", color=ColorsEnum.RED)
    token = jwt_hasher.encode(test_schema)
    tag_repository = TagRepository(session)
    tag_repository.create(token)

    assert tag_repository.get_by_token(token).token

def test_remove(session):
    test_schema = CategorySchema(name="Some test tag", color=ColorsEnum.RED)
    token = jwt_hasher.encode(test_schema)
    tag_repository = TagRepository(session)
    tag_repository.create(token)

    tag_repository.remove(token)

    assert tag_repository.get_by_token(token) is None

def test_update(session):
    test_schema = CategorySchema(name="Some test tag", color=ColorsEnum.RED)
    old_token = jwt_hasher.encode(test_schema)
    tag_repository = TagRepository(session)
    tag_repository.create(old_token)

    test_schema = CategorySchema(name="Some test tag123", color=ColorsEnum.RED)
    new_token = jwt_hasher.encode(test_schema)

    tag_repository.update(old_token, new_token)

    assert tag_repository.get_by_token(new_token).token == new_token
