from fastapi import APIRouter, Depends

from ..schemas import TaskSchema
from ..interactors.task_interactor import TaskInteractor
from ..repositories.task_repository import TaskRepository

from ..database import get_session_stub
from ..auth import get_hasher_stub

task_router = APIRouter(prefix='/tasks')


@task_router.get('/')
async def get_all_tasks(session = Depends(get_session_stub), hasher = Depends(get_hasher_stub)):
    task_repository = TaskRepository(session)
    task_interactor = TaskInteractor(task_repository, hasher)

    tasks = task_interactor.get_all_tasks()

    return tasks

@task_router.get('/{category_token}')
async def get_task_by_token(task_token, session = Depends(get_session_stub), hasher = Depends(get_hasher_stub)):
    task_repository = TaskRepository(session)
    task_interactor = TaskInteractor(task_repository, hasher)

    task = task_interactor.get_task_by_token(task_token)

    return task

@task_router.post('/')
async def create_task(task_schema: TaskSchema, session = Depends(get_session_stub), hasher = Depends(get_hasher_stub)):
    task_repository = TaskRepository(session)
    task_interactor = TaskInteractor(task_repository, hasher)

    task = task_interactor.create_task(task_schema)

    return task

@task_router.put('/')
async def update_task(old_task_schema: TaskSchema, new_task_schema: TaskSchema, session = Depends(get_session_stub), hasher = Depends(get_hasher_stub)):
    task_repository = TaskRepository(session)
    task_interactor = TaskInteractor(task_repository, hasher)

    task = task_interactor.update_task(old_task_schema, new_task_schema)

    return task

@task_router.delete('/')
async def delete_task(task_schema: TaskSchema, session = Depends(get_session_stub), hasher = Depends(get_hasher_stub)):
    task_repository = TaskRepository(session)
    task_interactor = TaskInteractor(task_repository, hasher)

    task = task_interactor.remove_task(task_schema)

    return task