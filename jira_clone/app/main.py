from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fastapi import FastAPI
import uvicorn

from .auth.hashing import get_hasher_stub, JWTHasher
from .database.database import get_session_stub, init

from .contollers import tag_router
from .contollers import task_router
from .contollers import user_router
from .contollers import category_router

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

        return jwt_hasher

    app.include_router(tag_router)
    app.include_router(user_router)
    app.include_router(category_router)
    app.include_router(task_router)

    app.dependency_overrides[get_session_stub] = get_session
    app.dependency_overrides[get_hasher_stub] = get_hasher

    uvicorn.run(app, host='0.0.0.0', port=8000)

if __name__ == '__main__':
    main()