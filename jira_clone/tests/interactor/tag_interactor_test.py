from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from jira_clone.app.database.database import Base
from jira_clone.app.repositories.tag_repository import TagRepository
from jira_clone.app.interactors.tag_interactor import TagInteractor

from jira_clone.app.schemas.schemas import TagSchema
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

def test_create_tag():
    tag_repository = TagRepository(get_session())
    tag_interactor = TagInteractor(tag_repository, jwt_hasher)

    tag_schema = TagSchema(
        name='Test Tag',
        color='red'
    )

    token = tag_interactor.create_tag(tag_schema)

    assert tag_interactor.get_tag_by_token(token) is not None

def test_remove_tag():
    tag_repository = TagRepository(get_session())
    tag_interactor = TagInteractor(tag_repository, jwt_hasher)

    tag_schema = TagSchema(
        name='Test Tag',
        color='red'
    )

    token = tag_interactor.remove_tag(tag_schema)

    assert tag_interactor.get_tag_by_token(token) is None

def test_update_tag():
    tag_repository = TagRepository(get_session())
    tag_interactor = TagInteractor(tag_repository, jwt_hasher)

    old_tag_schema = TagSchema(
        name='Test Tag',
        color='red'
    )

    new_tag_schema = TagSchema(
        name='Test Tag',
        color='blue'
    )

    tag_interactor.create_tag(old_tag_schema)
    token = tag_interactor.update_tag(old_tag_schema, new_tag_schema)

    assert token is not None