from pydantic import BaseModel, EmailStr
from enum import Enum

class ColorsEnum(str, Enum):
    RED: str = "red"
    GREEN: str = "green"
    BLUE: str = "blue"
    YELLOW: str = "yellow"
    PURPLE: str = "purple"
    CYAN: str = "cyan"
    WHITE: str = "white"
    BLACK: str = "black"


class UserSchema(BaseModel):
    first_name: str
    last_name: str

    username: str
    password: str
    email: EmailStr


class TaskSchema(BaseModel):
    title: str
    description: str

    creator: str
    performers: list
    tags: list


class TagSchema(BaseModel):
    name: str
    color: ColorsEnum


class CategorySchema(BaseModel):
    name: str
    color: ColorsEnum