from fastapi import Depends, APIRouter, HTTPException

from ..auth import get_hasher_stub
from ..database import get_session_stub
from ..interactors import CategoryInteractor
from ..repositories import CategoryRepository
from ..schemas import CategorySchema

category_router = APIRouter(prefix='/categories', tags=['categories'])

@category_router.get('/')
def get_all_tags(session=Depends(get_session_stub), hasher=Depends(get_hasher_stub)):
    category_repository = CategoryRepository(session)
    category_interactor = CategoryInteractor(category_repository, hasher)

    result = category_interactor.get_all()

    return result if result is not None else HTTPException(status_code=404)

@category_router.get('/{category_token}')
def get_category_by_token(category_token: str, session=Depends(get_session_stub), hasher=Depends(get_hasher_stub)):
    category_repository = CategoryRepository(session)
    category_interactor = CategoryInteractor(category_repository, hasher)

    result = category_interactor.get_by_token(category_token)

    return result if result is not None else HTTPException(status_code=404)


@category_router.post('/')
def create_category(category_schema: CategorySchema, session=Depends(get_session_stub), hasher=Depends(get_hasher_stub)):
    category_repository = CategoryRepository(session)
    category_interactor = CategoryInteractor(category_repository, hasher)

    result = category_interactor.create(category_schema)

    return result


@category_router.put('/')
def update_category(old_category_schema: CategorySchema, new_category_schema: CategorySchema, session=Depends(get_session_stub),
                hasher=Depends(get_hasher_stub)):
    category_repository = CategoryRepository(session)
    category_interactor = CategoryInteractor(category_repository, hasher)

    result = category_interactor.update(old_category_schema, new_category_schema)

    return result if result is not None else HTTPException(status_code=404)


@category_router.delete('/')
def delete_category(category_schema: CategorySchema, session=Depends(get_session_stub), hasher=Depends(get_hasher_stub)):
    category_repository = CategoryRepository(session)
    category_interactor = CategoryInteractor(category_repository, hasher)

    result = category_interactor.remove(category_schema)

    return result if result is not None else HTTPException(status_code=404)