from fastapi import APIRouter, Depends

from jira_clone.app.schemas import TagSchema
from jira_clone.app.database.database import get_session_stub
from jira_clone.app.auth.hashing import get_hasher_stub
from jira_clone.app.interactors.tag_interactor import TagInteractor
from jira_clone.app.repositories.tag_repository import TagRepository

tag_router = APIRouter(prefix='/tags')


@tag_router.get('/all')
async def get_all_tags(session = Depends(get_session_stub), hasher = Depends(get_hasher_stub)):
    tag_repository = TagRepository(session)
    tag_interactor = TagInteractor(tag_repository, hasher)

    tags = tag_interactor.get_all_tags()

    return tags

@tag_router.get('/find')
async def get_tag_by_token(tag_token, session = Depends(get_session_stub), hasher = Depends(get_hasher_stub)):
    tag_repository = TagRepository(session)
    tag_interactor = TagInteractor(tag_repository, hasher)

    tag = tag_interactor.get_tag_by_token(tag_token)

    return tag

@tag_router.post('/create')
async def create_tag(tag_schema: TagSchema, session = Depends(get_session_stub), hasher = Depends(get_hasher_stub)):
    tag_repository = TagRepository(session)
    tag_interactor = TagInteractor(tag_repository, hasher)

    tag = tag_interactor.create_tag(tag_schema)

    return tag

@tag_router.put('/update')
async def update_tag(old_tag_schema: TagSchema, new_tag_schema: TagSchema, session = Depends(get_session_stub), hasher = Depends(get_hasher_stub)):
    tag_repository = TagRepository(session)
    tag_interactor = TagInteractor(tag_repository, hasher)

    tag = tag_interactor.update_tag(old_tag_schema, new_tag_schema)

    return tag

@tag_router.delete('/delete')
async def delete_tag(tag_schema: TagSchema, session = Depends(get_session_stub), hasher = Depends(get_hasher_stub)):
    tag_repository = TagRepository(session)
    tag_interactor = TagInteractor(tag_repository, hasher)

    tag = tag_interactor.remove_tag(tag_schema)

    return tag