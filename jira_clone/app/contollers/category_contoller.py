from fastapi import APIRouter, Depends

from jira_clone.app.schemas import TagSchema
from jira_clone.app.database.database import get_session_stub
from jira_clone.app.auth.hashing import get_hasher_stub
from jira_clone.app.interactors.tag_interactor import TagInteractor
from jira_clone.app.repositories.tag_repository import TagRepository

category_router = APIRouter(prefix='/categories')


@category_router.get('/all')
async def get_all_categories(session = Depends(get_session_stub), hasher = Depends(get_hasher_stub)):
    category_repository = TagRepository(session)
    category_interactor = TagInteractor(category_repository, hasher)

    categories = category_interactor.get_all_categories()

    return categories

@category_router.get('/find')
async def get_category_by_token(category_token, session = Depends(get_session_stub), hasher = Depends(get_hasher_stub)):
    category_repository = TagRepository(session)
    category_interactor = TagInteractor(category_repository, hasher)

    category = category_interactor.get_category_by_token(category_token)

    return category

@category_router.post('/create')
async def create_category(category_schema: TagSchema, session = Depends(get_session_stub), hasher = Depends(get_hasher_stub)):
    category_repository = TagRepository(session)
    category_interactor = TagInteractor(category_repository, hasher)

    category = category_interactor.create_category(category_schema)

    return category

@category_router.put('/update')
async def update_category(old_category_schema: TagSchema, new_category_schema: TagSchema, session = Depends(get_session_stub), hasher = Depends(get_hasher_stub)):
    category_repository = TagRepository(session)
    category_interactor = TagInteractor(category_repository, hasher)

    category = category_interactor.update_category(old_category_schema, new_category_schema)

    return category

@category_router.delete('/delete')
async def delete_category(category_schema: TagSchema, session = Depends(get_session_stub), hasher = Depends(get_hasher_stub)):
    category_repository = TagRepository(session)
    category_interactor = TagInteractor(category_repository, hasher)

    category = category_interactor.remove_category(category_schema)

    return category