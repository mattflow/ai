from uuid import UUID, uuid4
from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    MappedAsDataclass,
    relationship,
)
from sqlalchemy.ext.asyncio import AsyncAttrs


class Model(DeclarativeBase, AsyncAttrs, MappedAsDataclass):
    pass


class UserModel(Model):
    __tablename__ = "user"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4, init=False)
    email: Mapped[str]
    projects: Mapped[list["ProjectModel"]] = relationship(
        back_populates="user", lazy="selectin"
    )


class ProjectModel(Model):
    __tablename__ = "project"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4, init=False)
    name: Mapped[str]
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"))
    user: Mapped["UserModel"] = relationship(back_populates="projects", lazy="joined")
