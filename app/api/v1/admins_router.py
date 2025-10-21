from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.jwt import get_current_admin, get_current_user
from app.crud import admin_crud
from app.database.base import get_db
from schemas.auth_schemas import UserUpdateSchema, UserResponseSchema

admins_router = APIRouter(prefix="/admin", tags=["Admins"])

@admins_router.get("/users", response_model=list[UserResponseSchema], summary="Get all users")
async def get_all_users(
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return await admin_crud.get_all_users(db)


@admins_router.get("/users/{user_id}", response_model=UserResponseSchema, summary="Get user by ID")
async def get_user_by_id(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return await admin_crud.get_user_by_id(user_id, db)


@admins_router.patch("/users/{user_id}", summary="Update user partially")
async def update_user(
    user_id: int,
    request: UserUpdateSchema,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return await admin_crud.update_user(user_id, request, current_user, db)



@admins_router.delete("/users/{user_id}", summary="Delete user")
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return await admin_crud.delete_user(user_id, db)
