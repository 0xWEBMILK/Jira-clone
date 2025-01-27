import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from jira_clone.app.database.database import Base
from jira_clone.app.repositories.tag_repository import TagRepository
from jira_clone.app.interactors.tag_interactor import TagInteractor
from jira_clone.app.schemas.schemas import TagSchema
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

def test_create_tag(session):
    tag_repository = TagRepository(session)
    tag_interactor = TagInteractor(tag_repository, jwt_hasher)
    tag_schema = TagSchema(name='Test Tag', color='red')
    token = tag_interactor.create(tag_schema)
    assert tag_interactor.get_by_token(token) is not None

def test_remove_tag(session):
    tag_repository = TagRepository(session)
    tag_interactor = TagInteractor(tag_repository, jwt_hasher)
    tag_schema = TagSchema(name='Test Tag', color='red')
    token = tag_interactor.remove(tag_schema)
    assert tag_interactor.get_by_token(token) is None

def test_update_tag(session):
    tag_repository = TagRepository(session)
    tag_interactor = TagInteractor(tag_repository, jwt_hasher)
    old_tag_schema = TagSchema(name='Test Tag', color='red')
    new_tag_schema = TagSchema(name='Test Tag', color='blue')
    tag_interactor.create(old_tag_schema)
    token = tag_interactor.update(old_tag_schema, new_tag_schema)
    assert token is not None
