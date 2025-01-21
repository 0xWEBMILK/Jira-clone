from fastapi import APIRouter, Depends

from jira_clone.app.schemas import TaskSchema
from jira_clone.app.database.database import get_session_stub
from jira_clone.app.auth.hashing import get_hasher_stub
from jira_clone.app.interactors.task_interactor import TaskInteractor
from jira_clone.app.repositories.task_repository import TaskRepository

task_router = APIRouter(prefix='/tasks')


@task_router.get('/all')
async def get_all_tasks(session = Depends(get_session_stub), hasher = Depends(get_hasher_stub)):
    task_repository = TaskRepository(session)
    task_interactor = TaskInteractor(task_repository, hasher)

    tasks = task_interactor.get_all_tasks()

    return tasks

@task_router.get('/find')
async def get_task_by_token(task_token, session = Depends(get_session_stub), hasher = Depends(get_hasher_stub)):
    task_repository = TaskRepository(session)
    task_interactor = TaskInteractor(task_repository, hasher)

    task = task_interactor.get_task_by_token(task_token)

    return task

@task_router.post('/create')
async def create_task(task_schema: TaskSchema, session = Depends(get_session_stub), hasher = Depends(get_hasher_stub)):
    task_repository = TaskRepository(session)
    task_interactor = TaskInteractor(task_repository, hasher)

    task = task_interactor.create_task(task_schema)

    return task

@task_router.put('/update')
async def update_task(old_task_schema: TaskSchema, new_task_schema: TaskSchema, session = Depends(get_session_stub), hasher = Depends(get_hasher_stub)):
    task_repository = TaskRepository(session)
    task_interactor = TaskInteractor(task_repository, hasher)

    task = task_interactor.update_task(old_task_schema, new_task_schema)

    return task

@task_router.delete('/delete')
async def delete_task(task_schema: TaskSchema, session = Depends(get_session_stub), hasher = Depends(get_hasher_stub)):
    task_repository = TaskRepository(session)
    task_interactor = TaskInteractor(task_repository, hasher)

    task = task_interactor.remove_task(task_schema)

    return task