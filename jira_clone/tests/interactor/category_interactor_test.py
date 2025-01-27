import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from jira_clone.app.database.database import Base
from jira_clone.app.repositories.category_repository import CategoryRepository
from jira_clone.app.interactors.category_interactor import CategoryInteractor
from jira_clone.app.schemas.schemas import CategorySchema
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

    session.close()
    Base.metadata.drop_all(engine)


def test_create_category(session):
    category_repository = CategoryRepository(session)
    category_interactor = CategoryInteractor(category_repository, jwt_hasher)

    category_schema = CategorySchema(
        name='Test Category',
        color='red'
    )

    token = category_interactor.create(category_schema)

    assert category_interactor.get_by_token(token) is not None

def test_remove_category(session):
    category_repository = CategoryRepository(session)
    category_interactor = CategoryInteractor(category_repository, jwt_hasher)

    category_schema = CategorySchema(
        name='Test Category',
        color='red'
    )

    token = category_interactor.remove(category_schema)

    assert category_interactor.get_by_token(token) is None

def test_update_category(session):
    category_repository = CategoryRepository(session)
    category_interactor = CategoryInteractor(category_repository, jwt_hasher)

    old_category_schema = CategorySchema(
        name='Test Category',
        color='red'
    )

    new_category_schema = CategorySchema(
        name='Test Category',
        color='blue'
    )

    category_interactor.create(old_category_schema)
    token = category_interactor.update(old_category_schema, new_category_schema)

    assert token is not None
