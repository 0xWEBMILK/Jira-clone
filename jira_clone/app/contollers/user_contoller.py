from fastapi import APIRouter, Depends

from jira_clone.app.schemas import UserSchema
from jira_clone.app.database.database import get_session_stub
from jira_clone.app.auth.hashing import get_hasher_stub
from jira_clone.app.interactors.user_interactor import UserInteractor
from jira_clone.app.repositories.user_repository import UserRepository

user_router = APIRouter(prefix='/users')


@user_router.get('/all')
async def get_all_users(session = Depends(get_session_stub), hasher = Depends(get_hasher_stub)):
    user_repository = UserRepository(session)
    user_interactor = UserInteractor(user_repository, hasher)

    users = user_interactor.get_all_users()

    return users

@user_router.get('/find')
async def get_user_by_token(user_token, session = Depends(get_session_stub), hasher = Depends(get_hasher_stub)):
    user_repository = UserRepository(session)
    user_interactor = UserInteractor(user_repository, hasher)

    user = user_interactor.get_user_by_token(user_token)

    return user

@user_router.post('/create')
async def create_user(user_schema: UserSchema, session = Depends(get_session_stub), hasher = Depends(get_hasher_stub)):
    user_repository = UserRepository(session)
    user_interactor = UserInteractor(user_repository, hasher)

    user = user_interactor.create_user(user_schema)

    return user

@user_router.put('/update')
async def update_user(old_user_schema: UserSchema, new_user_schema: UserSchema, session = Depends(get_session_stub), hasher = Depends(get_hasher_stub)):
    user_repository = UserRepository(session)
    user_interactor = UserInteractor(user_repository, hasher)

    user = user_interactor.update_user(old_user_schema, new_user_schema)

    return user

@user_router.delete('/delete')
async def delete_user(user_schema: UserSchema, session = Depends(get_session_stub), hasher = Depends(get_hasher_stub)):
    user_repository = UserRepository(session)
    user_interactor = UserInteractor(user_repository, hasher)

    user = user_interactor.remove_user(user_schema)

    return user