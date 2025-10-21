from sqlalchemy import select

from app.models.users import Users


async def get_user_by_email(email: str, db):
    query = select(Users).where(email == Users.email)
    res = await db.execute(query)
    user = res.scalar_one_or_none()
    return user

async def get_user_by_id(user_id: int, db):
    query = select(Users).where(user_id == Users.id)
    res = await db.execute(query)
    user = res.scalar_one_or_none()
    return user