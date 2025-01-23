from fastapi import Depends, APIRouter, HTTPException

from ..auth import get_hasher_stub
from ..database import get_session_stub
from ..interactors import UserInteractor
from ..repositories import UserRepository
from ..schemas import UserSchema

user_router = APIRouter(prefix='/users', tags=['users'])

@user_router.get('/')
def get_all_users(session=Depends(get_session_stub), hasher=Depends(get_hasher_stub)):
    user_repository = UserRepository(session)
    user_interactor = UserInteractor(user_repository, hasher)

    result = user_interactor.get_all()

    return result if result is not None else HTTPException(status_code=404)

@user_router.get('/{user_token}')
def get_user_by_token(user_token: str, session=Depends(get_session_stub), hasher=Depends(get_hasher_stub)):
    user_repository = UserRepository(session)
    user_interactor = UserInteractor(user_repository, hasher)

    result = user_interactor.get_by_token(user_token)

    return result if result is not None else HTTPException(status_code=404)


@user_router.post('/')
def create_user(user_schema: UserSchema, session=Depends(get_session_stub), hasher=Depends(get_hasher_stub)):
    user_repository = UserRepository(session)
    user_interactor = UserInteractor(user_repository, hasher)

    result = user_interactor.create(user_schema)

    return result


@user_router.put('/')
def update_user(old_schema: UserSchema, new_schema: UserSchema, session=Depends(get_session_stub),
                hasher=Depends(get_hasher_stub)):
    user_repository = UserRepository(session)
    user_interactor = UserInteractor(user_repository, hasher)

    result = user_interactor.update(old_schema, new_schema)

    return result if result is not None else HTTPException(status_code=404)


@user_router.delete('/')
def delete_user(user_schema: UserSchema, session=Depends(get_session_stub), hasher=Depends(get_hasher_stub)):
    user_repository = UserRepository(session)
    user_interactor = UserInteractor(user_repository, hasher)

    result = user_interactor.remove(user_schema)

    return result if result is not None else HTTPException(status_code=404)