from datetime import datetime

from pydantic import BaseModel, Field, EmailStr

from typing import Optional

class LoginSchema(BaseModel):
    email: str = Field(..., examples=["example@gmail.com"])
    password: str

class CreateAdminSchema(BaseModel):
    email: str = Field(..., examples=["info@gmail.com"])
    password: str

class CreateUserSchema(BaseModel):
    email: str = Field(..., examples=["example@gmail.com"])
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: str = Field(..., min_length=8)

class VerifyVerificationCodeSchema(BaseModel):
    email: str = Field(..., examples=["example@gmail.com"])
    code: str = Field(..., min_length=4, max_length=4)


class UserResponseSchema(BaseModel):
    id: int
    email: EmailStr
    first_name: str | None
    last_name: str | None
    role: str
    is_verified: bool
    created_at: datetime

    class Config:
        orm_mode = True


class UserUpdateSchema(BaseModel):
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    password: str | None = None