from typing import Annotated
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import SessionDep
from app.models import UserModel


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self):
        result = await self.session.scalars(select(UserModel))
        return result.all()


def get_user_service(session: SessionDep):
    return UserService(session)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
