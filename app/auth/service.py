from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.auth.security import verify_password_async
from app.models.user import User


async def authenticate_user(
    db: AsyncSession,
    email: str,
    password: str,
) -> User | None:
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if not user:
        return None

    if not await verify_password_async(password, user.hashed_password):
        return None

    return user
