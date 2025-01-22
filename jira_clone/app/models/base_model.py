from sqlalchemy.orm import declarative_base, Mapped, mapped_column

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[str] = mapped_column(unique=True, nullable=False)