from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.base import get_db
from app.crud import auth_crud
from schemas.auth_schemas import CreateUserSchema, VerifyVerificationCodeSchema, LoginSchema

auth_router = APIRouter()

@auth_router.post("/signup", summary="Sign Up User", description="Registration for user, sends verification code to your email.")
async def signup_user(request: CreateUserSchema, db: AsyncSession = Depends(get_db)):
    return await auth_crud.create_user(request, db)

@auth_router.post("/login", summary="Login", description="Login API for both user and admin")
async def login(request: LoginSchema, db: AsyncSession = Depends(get_db)):
    return await auth_crud.login_user(request, db)

@auth_router.post("/verify", summary="Verify User", description="Endpoint to verify user with sent code to the email.")
async def verify_user(request: VerifyVerificationCodeSchema, db: AsyncSession = Depends(get_db)):
    return await auth_crud.verify_verification_code(request.code, request.email, db)