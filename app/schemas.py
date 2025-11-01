from uuid import UUID
from pydantic import BaseModel, ConfigDict, EmailStr


class Schema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UserPublicSchema(Schema):
    id: UUID
    email: EmailStr
