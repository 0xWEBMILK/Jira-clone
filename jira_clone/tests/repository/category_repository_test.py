import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from jira_clone.app.database.database import Base
from jira_clone.app.repositories.category_repository import CategoryRepository
from jira_clone.app.schemas.schemas import CategorySchema, ColorsEnum
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
    session.rollback()
    session.close()
    Base.metadata.drop_all(engine)

def test_create(session):
    test_schema = CategorySchema(name="Some test category", color=ColorsEnum.RED)
    token = jwt_hasher.encode(test_schema)
    category_repository = CategoryRepository(session)
    category_repository.create(token)

    assert category_repository.get_by_token(token).token

def test_remove(session):
    test_schema = CategorySchema(name="Some test category", color=ColorsEnum.RED)
    token = jwt_hasher.encode(test_schema)
    category_repository = CategoryRepository(session)
    category_repository.create(token)

    category_repository.remove(token)

    assert category_repository.get_by_token(token) is None

def test_update(session):
    test_schema = CategorySchema(name="Some test category", color=ColorsEnum.RED)
    old_token = jwt_hasher.encode(test_schema)
    category_repository = CategoryRepository(session)
    category_repository.create(old_token)

    test_schema = CategorySchema(name="Some test category123", color=ColorsEnum.RED)
    new_token = jwt_hasher.encode(test_schema)

    category_repository.update(old_token, new_token)

    assert category_repository.get_by_token(new_token).token == new_token
