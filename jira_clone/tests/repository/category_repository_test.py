import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from jira_clone.app.database.database import Base
from jira_clone.app.repositories.category_repository import CategoryRepository
from jira_clone.app.schemas.schemas import CategorySchema, ColorsEnum
from jira_clone.app.auth.hashing import JWTHasher

jwt_hasher = JWTHasher('super', 'HS256')

@pytest.fixture(scope='function')
def session():
    engine = create_engine('sqlite:///test.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.rollback()
    session.close()
    Base.metadata.drop_all(engine)

@pytest.fixture
def category_repository(session):
    return CategoryRepository(session)

def test_create(category_repository):
    test_schema = CategorySchema(
        name="Some test category",
        color=ColorsEnum.RED
    )
    token = jwt_hasher.encode(test_schema)
    category_repository.create(token)
    assert category_repository.get_by_token(token).token

def test_remove(category_repository):
    test_schema = CategorySchema(
        name="Some test category",
        color=ColorsEnum.RED
    )
    token = jwt_hasher.encode(test_schema)
    category_repository.create(token)
    category_repository.remove(token)
    assert category_repository.get_by_token(token) is None

def test_update(category_repository):
    test_schema = CategorySchema(
        name="Some test category",
        color=ColorsEnum.RED
    )
    old_token = jwt_hasher.encode(test_schema)
    category_repository.create(old_token)

    test_schema = CategorySchema(
        name="Some test category123",
        color=ColorsEnum.RED
    )
    new_token = jwt_hasher.encode(test_schema)
    category_repository.update(old_token, new_token)

    assert category_repository.get_by_token(new_token).token == new_token
