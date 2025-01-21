from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from jira_clone.app.database.database import Base
from jira_clone.app.repositories.category_repository import CategoryRepository
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


def test_create_category():
    test_category_schema = CategorySchema(
        name="Some test category",
        color=ColorsEnum.RED
    )

    token = jwt_hasher_interface.encode(test_category_schema)
    category_repository = CategoryRepository(get_session())
    category_repository.create_category(token)

    assert category_repository.get_category_by_token(token).token

def test_remove_category():
    test_category_schema = CategorySchema(
        name="Some test category",
        color=ColorsEnum.RED
    )

    token = jwt_hasher_interface.encode(test_category_schema)
    category_repository = CategoryRepository(get_session())
    category_repository.remove_category(token)

    assert category_repository.get_category_by_token(token) is None

def test_update_category():
    test_category_schema = CategorySchema(
        name="Some test category",
        color=ColorsEnum.RED
    )

    old_token = jwt_hasher_interface.encode(test_category_schema)
    category_repository = CategoryRepository(get_session())

    category_repository.create_category(old_token)

    test_category_schema = CategorySchema(
        name="Some test category123",
        color=ColorsEnum.RED
    )

    new_token = jwt_hasher_interface.encode(test_category_schema)

    category_repository.update_category(old_token, new_token)

    assert category_repository.get_category_by_token(new_token).token == new_token
