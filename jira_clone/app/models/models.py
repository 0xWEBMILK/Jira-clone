from sqlalchemy.orm import Mapped, mapped_column
from .base_model import BaseModel

class UserModel(BaseModel):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[str] = mapped_column(unique=True, nullable=False)

class TaskModel(BaseModel):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[str] = mapped_column(unique=True, nullable=False)

class TagModel(BaseModel):
    __tablename__ = 'tags'

    id: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[str] = mapped_column(unique=True, nullable=False)

class CategoryModel(BaseModel):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[str] = mapped_column(unique=True, nullable=False)