from pydantic import BaseModel, EmailStr

class User(BaseModel):
    first_name: str
    last_name: str

    username: str
    password: str
    email: EmailStr

class Task(BaseModel):
    title: str
    description: str

    creator: str
    performers: list
    tags: list
