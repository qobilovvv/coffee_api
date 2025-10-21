from datetime import datetime, timedelta, timezone
from app.core.celery_app import celery
from sqlalchemy.future import select

from app.database.base import AsyncSessionLocal
from app.models import Users


@celery.task(name="app.tasks.cleanup.delete_unverified_users")
def delete_unverified_users():
    import asyncio
    asyncio.run(_delete_unverified_users_async())


# deletes users who signed up, but not verified
async def _delete_unverified_users_async():
    async with AsyncSessionLocal() as session:
        two_days_ago = datetime.now(timezone.utc) - timedelta(days=2)
        result = await session.execute(
            select(Users).where(Users.is_verified == False, Users.created_at < two_days_ago)
        )
        users = result.scalars().all()
        for user in users:
            await session.delete(user)
            print(f"[Celery] Deleted unverified user: {user.email}")
        await session.commit()
