from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

from app.models.user import User, UserRole
from app.users.repository import UserRepository
from app.users.schemas import UserCreate, UserRoleUpdate, UserUpdate
from app.auth.security import hash_password_async
from app.wallet.service import WalletService


class UserService:

    def __init__(self, repository: UserRepository, wallet_service: WalletService):
        self.repository = repository
        self.wallet_service = wallet_service

    async def create_user(self, db: AsyncSession, user_data: UserCreate) -> User:
        exist = await self.repository.get_by_email(db, user_data.email)
        if exist:
            raise HTTPException(status_code=400, detail="Email already registered")

        user = User(
            email=user_data.email,
            hashed_password=await hash_password_async(user_data.password),
            role=user_data.role,
        )

        await self.repository.create(db, user)
        await self.wallet_service.create_wallet(db, user.id)
        await db.commit()
        await db.refresh(user)
        return user

    async def get_user_by_id(self, db: AsyncSession, user_id: int) -> User:
        user = await self.repository.get_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    async def get_all_users(self, db: AsyncSession) -> list[User]:
        return await self.repository.get_all(db)

    async def get_me(self, db: AsyncSession, user_id: int) -> User:
        return await self.get_user_by_id(db, user_id)

    async def update_me(self, db: AsyncSession, user_id: int, data: UserUpdate) -> User:
        user = await self.get_user_by_id(db, user_id)
        result = await self.repository.update_user(db, user, data)
        await db.commit()
        return result

    async def update_role(self, db: AsyncSession, user_id: int, data: UserRoleUpdate) -> User:
        user = await self.get_user_by_id(db, user_id)
        result = await self.repository.update_role_user(db, user, data.role)
        await db.commit()
        return result

    async def get_assigned_tasks(self, db: AsyncSession, user_id: int):
        user = await self.get_user_by_id(db, user_id)
        if user.role != UserRole.EXECUTOR:
            raise HTTPException(status_code=403, detail="Only executors have assigned tasks")
        return await self.repository.get_assigned_tasks(db, user_id)