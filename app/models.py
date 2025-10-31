from uuid import UUID, uuid4
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, MappedAsDataclass
from sqlalchemy.ext.asyncio import AsyncAttrs


class Model(DeclarativeBase, AsyncAttrs, MappedAsDataclass):
    pass


class UserModel(Model):
    __tablename__ = "user"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4, init=False)
    email: Mapped[str]
