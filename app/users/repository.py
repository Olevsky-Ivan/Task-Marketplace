from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User, UserRole
from app.models.task import Task
from app.users.schemas import UserUpdate
from app.auth.security import hash_password_async


class UserRepository:

    async def get_all(self, db: AsyncSession) -> list[User]:
        result = await db.execute(select(User))
        return result.scalars().all()

    async def get_by_id(self, db: AsyncSession, user_id: int) -> User | None:
        return await db.get(User, user_id)

    async def get_by_email(self, db: AsyncSession, email: str) -> User | None:
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def create(self, db: AsyncSession, user: User) -> User:
        db.add(user)
        await db.flush()
        await db.refresh(user)
        return user

    async def update_user(self, db: AsyncSession, user: User, data: UserUpdate) -> User:
        if data.email is not None:
            user.email = data.email
        if data.password is not None:
            user.hashed_password = await hash_password_async(data.password)

        await db.flush()
        await db.refresh(user)
        return user

    async def update_role_user(
        self, db: AsyncSession, user: User, role: UserRole
    ) -> User:
        user.role = role
        await db.flush()
        await db.refresh(user)
        return user

    async def get_assigned_tasks(self, db: AsyncSession, user_id: int) -> list[Task]:
        result = await db.execute(select(Task).where(Task.executor_id == user_id))
        return result.scalars().all()
