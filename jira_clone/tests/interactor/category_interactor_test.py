from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from jira_clone.app.database.database import Base
from jira_clone.app.repositories.category_repository import CategoryRepository
from jira_clone.app.interactors.category_interactor import CategoryInteractor

from jira_clone.app.schemas.schemas import CategorySchema
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

def test_create_category():
    category_repository = CategoryRepository(get_session())
    category_interactor = CategoryInteractor(category_repository, jwt_hasher)

    category_schema = CategorySchema(
        name='Test Category',
        color='red'
    )

    token = category_interactor.create_category(category_schema)

    assert category_interactor.get_category_by_token(token) is not None

def test_remove_category():
    category_repository = CategoryRepository(get_session())
    category_interactor = CategoryInteractor(category_repository, jwt_hasher)

    category_schema = CategorySchema(
        name='Test Category',
        color='red'
    )

    token = category_interactor.remove_category(category_schema)

    assert category_interactor.get_category_by_token(token) is None

def test_update_category():
    category_repository = CategoryRepository(get_session())
    category_interactor = CategoryInteractor(category_repository, jwt_hasher)

    old_category_schema = CategorySchema(
        name='Test Category',
        color='red'
    )

    new_category_schema = CategorySchema(
        name='Test Category',
        color='blue'
    )

    category_interactor.create_category(old_category_schema)
    token = category_interactor.update_category(old_category_schema, new_category_schema)

    assert token is not None