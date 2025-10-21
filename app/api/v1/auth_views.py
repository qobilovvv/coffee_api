from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.jwt import get_current_user
from app.database.base import get_db
from app.crud import auth_crud
from schemas.auth_schemas import CreateUserSchema, VerifyVerificationCodeSchema, LoginSchema, CreateAdminSchema

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

# Create admin api, we can delete it and use it's crud, inner function that creates admin
@auth_router.post("/create-admin", summary="Create Admin API", description="Create admin api, we can delete it and use it's crud, inner function that creates admin")
async def create_admin(request: CreateAdminSchema, db: AsyncSession = Depends(get_db)):
    return await auth_crud.create_admin(request, db)

@auth_router.post("/me", summary="Get Me API", description="Get data about user")
async def get_me(current_user = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "role": current_user.role
    }