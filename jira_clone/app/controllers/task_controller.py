from fastapi import Depends, APIRouter, HTTPException

from ..auth import get_hasher_stub
from ..database import get_session_stub
from ..interactors import TaskInteractor
from ..repositories import TaskRepository
from ..schemas import TaskSchema

task_router = APIRouter(prefix='/tasks', tags=['tasks'])

@task_router.get('/', status_code=200)
def get_all_tasks(session=Depends(get_session_stub), hasher=Depends(get_hasher_stub)):
    task_repository = TaskRepository(session)
    task_interactor = TaskInteractor(task_repository, hasher)

    result = task_interactor.get_all()

    return result if result is not None else HTTPException(status_code=404)

@task_router.get('/{task_token}', status_code=200)
def get_task_by_token(task_token: str, session = Depends(get_session_stub), hasher = Depends(get_hasher_stub)):
    task_repository = TaskRepository(session)
    task_interactor = TaskInteractor(task_repository, hasher)

    result = task_interactor.get_by_token(task_token)

    return result if result is not None else HTTPException(status_code=404)

@task_router.post('/', status_code=201)
def create_task(task_schema: TaskSchema, session = Depends(get_session_stub), hasher = Depends(get_hasher_stub)):
    task_repository = TaskRepository(session)
    task_interactor = TaskInteractor(task_repository, hasher)

    result = task_interactor.create(task_schema)

    return result

@task_router.put('/', status_code=201)
def update_task(old_schema: TaskSchema, new_schema: TaskSchema, session = Depends(get_session_stub), hasher = Depends(get_hasher_stub)):
    task_repository = TaskRepository(session)
    task_interactor = TaskInteractor(task_repository, hasher)

    result = task_interactor.update(old_schema, new_schema)

    return result if result is not None else HTTPException(status_code=404)

@task_router.delete('/', status_code=200)
def delete_task(task_schema: TaskSchema, session = Depends(get_session_stub), hasher = Depends(get_hasher_stub)):
    task_repository = TaskRepository(session)
    task_interactor = TaskInteractor(task_repository, hasher)

    result = task_interactor.remove(task_schema)

    return result if result is not None else HTTPException(status_code=404)