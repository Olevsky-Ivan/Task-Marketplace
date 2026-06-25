from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user, require_role
from app.database.session import get_db
from app.models.user import User, UserRole
from app.users.service import UserService
from app.users.repository import UserRepository
from app.users.schemas import UserRead, UserUpdate, UserRoleUpdate
from app.tasks.schemas import TaskRead
from app.wallet.service import WalletService
from app.wallet.repository import WalletRepository

router = APIRouter()

user_service = UserService(
    repository=UserRepository(),
    wallet_service=WalletService(repository=WalletRepository()),
)


@router.get("/me", response_model=UserRead)
async def get_me(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await user_service.get_me(db, current_user.id)


@router.put("/me", response_model=UserRead)
async def update_me(
    body: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await user_service.update_me(db, current_user.id, body)


@router.get("/me/tasks", response_model=list[TaskRead])
async def get_my_tasks(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await user_service.get_assigned_tasks(db, current_user.id)


@router.get("/", response_model=list[UserRead])
async def get_all_users(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.ADMIN)),
):
    return await user_service.get_all_users(db)


@router.get("/{user_id}", response_model=UserRead)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await user_service.get_user_by_id(db, user_id)


@router.put("/{user_id}/role", response_model=UserRead)
async def update_role(
    user_id: int,
    body: UserRoleUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.ADMIN)),
):
    return await user_service.update_role(db, user_id, body)