from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fastapi import FastAPI
import uvicorn

from jira_clone.app.auth.hashing import get_hasher_stub
from jira_clone.app.database.database import get_session_stub, init
from auth.hashing import JWTHasher, HasherInterface

from contollers.tag_contoller import tag_router
from contollers.task_contoller import task_router
from contollers.user_contoller import user_router
from contollers.category_contoller import category_router

def main():
    app = FastAPI()
    engine = create_engine('sqlite:///jira.db')
    session = sessionmaker(bind=engine)
    init(engine)

    def get_session():
        with session() as s:
            try:
                yield s
            except Exception as e:
                s.rollback()
                raise e
            finally:
                s.close()

    def get_hasher():
        jwt_hasher = JWTHasher(key='super', alg='HS256')
        jwt_hasher_interface = HasherInterface(jwt_hasher)

        return jwt_hasher_interface

    app.include_router(tag_router)
    app.include_router(user_router)
    app.include_router(category_router)
    app.include_router(task_router)

    app.dependency_overrides[get_session_stub] = get_session
    app.dependency_overrides[get_hasher_stub] = get_hasher

    uvicorn.run(app, host='0.0.0.0', port=8000)

if __name__ == '__main__':
    main()