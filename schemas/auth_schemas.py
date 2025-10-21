from pydantic import BaseModel, Field

from typing import Optional

class LoginSchema(BaseModel):
    email: str = Field(..., examples=["example@gmail.com"])
    password: str

class CreateUserSchema(BaseModel):
    email: str = Field(..., examples=["example@gmail.com"])
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: str = Field(..., min_length=8)

class VerifyVerificationCodeSchema(BaseModel):
    email: str = Field(..., examples=["example@gmail.com"])
    code: str = Field(..., min_length=4, max_length=4)