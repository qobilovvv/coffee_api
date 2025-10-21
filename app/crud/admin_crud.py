from fastapi import HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.jwt import hash_password
from app.crud.common import get_user_by_email
from app.models import Users
from schemas.auth_schemas import UserUpdateSchema


async def get_all_users(db: AsyncSession):
    result = await db.execute(select(Users))
    return result.scalars().all()


async def get_user_by_id(user_id: int, db: AsyncSession):
    result = await db.execute(select(Users).where(Users.id == user_id))
    return result.scalars().first()


async def update_user(user_id: int, request: UserUpdateSchema, current_user, db: AsyncSession):
    user = await get_user_by_id(user_id, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # checking if user want to change email and is there any email like the one user wants
    if request.email:
        existing_email = await get_user_by_email(request.email, db)
        if existing_email and existing_email.id != user.id:
            raise HTTPException(status_code=400, detail="Email already exists")

    # if you are not admin and it is not your profile which you wanna change, you cannot do it
    if current_user.role != "ADMIN" and current_user.id != user.id:
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to edit other users' profiles"
        )

    update_data = request.model_dump(exclude_unset=True)

    if "password" in update_data:
        update_data["password"] = hash_password(update_data["password"])

    for field, value in update_data.items():
        setattr(user, field, value)

    await db.commit()
    await db.refresh(user)

    return {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "role": user.role,
    }


async def delete_user(user_id: int, db: AsyncSession):
    user = await get_user_by_id(user_id, db)
    if not user:
        raise HTTPException(detail="No User Found", status_code=404)

    await db.delete(user)
    await db.commit()
    return {
        "message": "deleted successfully"
    }
