from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime

# these are the pydantic base model which is come from the request body
class CreateUserSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    phone: str | None = None
    role_id: int

class UpdateUserSchema(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None
    role_id: int | None = None
    is_active: bool | None = None

class UserResponseSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone: str | None
    role_name: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )
    