from fastapi import Depends, APIRouter, HTTPException

from ..auth import get_hasher_stub
from ..database import get_session_stub
from ..interactors import TagInteractor
from ..repositories import TagRepository
from ..schemas import TagSchema

tag_router = APIRouter(prefix='/tags', tags=['tags'])

@tag_router.get('/')
def get_all_tags(session=Depends(get_session_stub), hasher=Depends(get_hasher_stub)):
    tag_repository = TagRepository(session)
    tag_interactor = TagInteractor(tag_repository, hasher)

    result = tag_interactor.get_all()

    return result if result is not None else HTTPException(status_code=404)

@tag_router.get('/{tag_token}')
def get_tag_by_token(tag_token: str, session=Depends(get_session_stub), hasher=Depends(get_hasher_stub)):
    tag_repository = TagRepository(session)
    tag_interactor = TagInteractor(tag_repository, hasher)

    result = tag_interactor.get_by_token(tag_token)

    return result if result is not None else HTTPException(status_code=404)


@tag_router.post('/')
def create_tag(tag_schema: TagSchema, session=Depends(get_session_stub), hasher=Depends(get_hasher_stub)):
    tag_repository = TagRepository(session)
    tag_interactor = TagInteractor(tag_repository, hasher)

    result = tag_interactor.create(tag_schema)

    return result if result is not None else HTTPException(status_code=404)


@tag_router.put('/')
def update_tag(old_schema: TagSchema, new_schema: TagSchema, session=Depends(get_session_stub),
                hasher=Depends(get_hasher_stub)):
    tag_repository = TagRepository(session)
    tag_interactor = TagInteractor(tag_repository, hasher)

    result = tag_interactor.update(old_schema, new_schema)

    return result if result is not None else HTTPException(status_code=404)


@tag_router.delete('/')
def delete_tag(tag_schema: TagSchema, session=Depends(get_session_stub), hasher=Depends(get_hasher_stub)):
    tag_repository = TagRepository(session)
    tag_interactor = TagInteractor(tag_repository, hasher)

    result = tag_interactor.remove(tag_schema)

    return result if result is not None else HTTPException(status_code=404)