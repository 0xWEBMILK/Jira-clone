from fastapi import APIRouter, Depends, HTTPException

from ..schemas import CategorySchema
from ..interactors import CategoryInteractor
from ..repositories import CategoryRepository


from ..database import get_session_stub
from ..auth import get_hasher_stub

category_router = APIRouter(prefix='/categories')


@category_router.get('/')
async def get_all_categories(session = Depends(get_session_stub), hasher = Depends(get_hasher_stub)):
    category_repository = CategoryRepository(session)
    category_interactor = CategoryInteractor(category_repository, hasher)

    categories = category_interactor.get_all_categories()

    return categories

@category_router.get('/{category_token}')
async def get_category_by_token(category_token, session = Depends(get_session_stub), hasher = Depends(get_hasher_stub)):
    category_repository = CategoryRepository(session)
    category_interactor = CategoryInteractor(category_repository, hasher)

    category = category_interactor.get_category_by_token(category_token)

    return category if category != 404 else HTTPException(status_code=404)

@category_router.post('/')
async def create_category(category_schema: CategorySchema, session = Depends(get_session_stub), hasher = Depends(get_hasher_stub)):
    category_repository = CategoryRepository(session)
    category_interactor = CategoryInteractor(category_repository, hasher)

    category = category_interactor.create_category(category_schema)

    return category

@category_router.put('/')
async def update_category(old_category_schema: CategorySchema, new_category_schema: CategorySchema, session = Depends(get_session_stub), hasher = Depends(get_hasher_stub)):
    category_repository = CategoryRepository(session)
    category_interactor = CategoryInteractor(category_repository, hasher)

    category = category_interactor.update_category(old_category_schema, new_category_schema)

    return category if category != 404 else HTTPException(status_code=404)

@category_router.delete('/')
async def delete_category(category_schema: CategorySchema, session = Depends(get_session_stub), hasher = Depends(get_hasher_stub)):
    category_repository = CategoryRepository(session)
    category_interactor = CategoryInteractor(category_repository, hasher)

    category = category_interactor.remove_category(category_schema)

    return category if category != 404 else HTTPException(status_code=404)