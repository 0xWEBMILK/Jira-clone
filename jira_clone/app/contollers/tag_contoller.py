from fastapi import APIRouter, Depends, HTTPException

from ..schemas import TagSchema
from ..interactors.tag_interactor import TagInteractor
from ..repositories.tag_repository import TagRepository

from ..database import get_session_stub
from ..auth import get_hasher_stub

tag_router = APIRouter(prefix='/tags')


@tag_router.get('/')
async def get_all_tags(session = Depends(get_session_stub), hasher = Depends(get_hasher_stub)):
    tag_repository = TagRepository(session)
    tag_interactor = TagInteractor(tag_repository, hasher)

    tags = tag_interactor.get_all_tags()

    return tags

@tag_router.get('/{category_token}')
async def get_tag_by_token(tag_token, session = Depends(get_session_stub), hasher = Depends(get_hasher_stub)):
    tag_repository = TagRepository(session)
    tag_interactor = TagInteractor(tag_repository, hasher)

    tag = tag_interactor.get_tag_by_token(tag_token)

    return tag if tag != 404 else HTTPException(status_code=404)

@tag_router.post('/')
async def create_tag(tag_schema: TagSchema, session = Depends(get_session_stub), hasher = Depends(get_hasher_stub)):
    tag_repository = TagRepository(session)
    tag_interactor = TagInteractor(tag_repository, hasher)

    tag = tag_interactor.create_tag(tag_schema)

    return tag

@tag_router.put('/')
async def update_tag(old_tag_schema: TagSchema, new_tag_schema: TagSchema, session = Depends(get_session_stub), hasher = Depends(get_hasher_stub)):
    tag_repository = TagRepository(session)
    tag_interactor = TagInteractor(tag_repository, hasher)

    tag = tag_interactor.update_tag(old_tag_schema, new_tag_schema)

    return tag if tag != 404 else HTTPException(status_code=404)

@tag_router.delete('/')
async def delete_tag(tag_schema: TagSchema, session = Depends(get_session_stub), hasher = Depends(get_hasher_stub)):
    tag_repository = TagRepository(session)
    tag_interactor = TagInteractor(tag_repository, hasher)

    tag = tag_interactor.remove_tag(tag_schema)

    return tag if tag != 404 else HTTPException(status_code=404)