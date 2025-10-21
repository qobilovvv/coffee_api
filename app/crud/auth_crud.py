from datetime import datetime, timezone, timedelta
from random import randint

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.jwt import hash_password, verify_password, create_access_token, create_refresh_token
from app.crud.common import get_user_by_email
from app.models import Users
from schemas.auth_schemas import CreateUserSchema, LoginSchema, CreateAdminSchema


# Create User function
async def create_user(request: CreateUserSchema, db: AsyncSession):
    # check uniquiness of email
    user = await get_user_by_email(request.email, db)
    if user:
        raise HTTPException(detail="User already exists", status_code=400)

    code = randint(1000, 9999)

    new_user = Users(
        email=request.email,
        first_name=getattr(request, "first_name", None),
        last_name=getattr(request, "last_name", None),
        password=hash_password(request.password),
        verification_code=str(code)
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    # printing the code in konsole. (I would add smtp)
    print(f"Verification code for {new_user.email} -> {code}")

    return {
        "email": new_user.email,
        "user_status": "not verified",
        "message": "Check your email, we sent verification code to it"
    }

async def create_admin(request: CreateAdminSchema, db: AsyncSession):
    user = get_user_by_email(request.email, db)
    if user:
        raise HTTPException(detail="User already exists", status_code=400)

    new_user = Users(
        email=request.email,
        password=hash_password(request.password),
        role="ADMIN"
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return {
        "email": new_user.email,
        "role": new_user.role
    }


async def login_user(request: LoginSchema, db: AsyncSession):
    user = await get_user_by_email(request.email, db)
    if not user:
        raise HTTPException(detail="No User Found", status_code=404)

    if not verify_password(request.password, user.password):
        raise HTTPException(detail="Invalid Credentials", status_code=400)

    payload = {
        "sub": str(user.id),
        "role": str(user.role),
    }

    return {
        "access_token": create_access_token(payload),
        "refresh_token": create_refresh_token(payload),
    }


async def verify_verification_code(verification_code: str, email: str, db: AsyncSession):
    user = await get_user_by_email(email, db)
    # check if there is such user
    if not user:
        raise HTTPException(detail="No User found", status_code=404)

    # checking if user already verified
    if user.is_verified:
        return {"message": "you already verified"}
    # checking the code
    if user.verification_code != verification_code:
        raise HTTPException(detail="Invalid credentials", status_code=400)
    # checking isn't the code is expired
    elapsed = datetime.now(timezone.utc) - (user.verification_code_created_at.replace(tzinfo=timezone.utc))
    if elapsed > timedelta(minutes=5):
        raise HTTPException(status_code=400, detail="Verification code expired")


    user.is_verified = True
    user.verification_code = None
    await db.commit()

    return {
        "message": "User verified successfully",
        "user_status": "verified"
    }
