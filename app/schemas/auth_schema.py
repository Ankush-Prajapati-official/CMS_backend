from pydantic import BaseModel, EmailStr, ConfigDict


class LoginSchema(BaseModel):
    email: EmailStr
    password: str

class ForgotPasswordSchema(BaseModel):
    email: EmailStr

class ResetPasswordSchema(BaseModel):
    token: str
    new_password: str

class ChangePasswordSchema(BaseModel):
    old_password: str
    new_password: str


class UpdateProfileSchema(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None

class RefreshTokenSchema(BaseModel):
    refresh_token: str