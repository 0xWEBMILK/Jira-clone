from fastapi import APIRouter, Depends

from ..schemas import UserSchema
from ..interactors.user_interactor import UserInteractor
from ..repositories.user_repository import UserRepository

from ..database import get_session_stub
from ..auth import get_hasher_stub

user_router = APIRouter(prefix='/users')


@user_router.get('/')
async def get_all_users(session = Depends(get_session_stub), hasher = Depends(get_hasher_stub)):
    user_repository = UserRepository(session)
    user_interactor = UserInteractor(user_repository, hasher)

    users = user_interactor.get_all_users()

    return users

@user_router.get('/{category_token}')
async def get_user_by_token(user_token, session = Depends(get_session_stub), hasher = Depends(get_hasher_stub)):
    user_repository = UserRepository(session)
    user_interactor = UserInteractor(user_repository, hasher)

    user = user_interactor.get_user_by_token(user_token)

    return user

@user_router.post('/')
async def create_user(user_schema: UserSchema, session = Depends(get_session_stub), hasher = Depends(get_hasher_stub)):
    user_repository = UserRepository(session)
    user_interactor = UserInteractor(user_repository, hasher)

    user = user_interactor.create_user(user_schema)

    return user

@user_router.put('/')
async def update_user(old_user_schema: UserSchema, new_user_schema: UserSchema, session = Depends(get_session_stub), hasher = Depends(get_hasher_stub)):
    user_repository = UserRepository(session)
    user_interactor = UserInteractor(user_repository, hasher)

    user = user_interactor.update_user(old_user_schema, new_user_schema)

    return user

@user_router.delete('/')
async def delete_user(user_schema: UserSchema, session = Depends(get_session_stub), hasher = Depends(get_hasher_stub)):
    user_repository = UserRepository(session)
    user_interactor = UserInteractor(user_repository, hasher)

    user = user_interactor.remove_user(user_schema)

    return user