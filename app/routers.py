from fastapi import APIRouter

from app.schemas import UserPublicSchema
from app.services import UserServiceDep

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.get("/", response_model=list[UserPublicSchema])
async def get_users(user_service: UserServiceDep):
    return await user_service.get_all()
