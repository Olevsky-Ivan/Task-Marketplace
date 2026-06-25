from datetime import datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user
from app.database.session import get_db
from app.models.user import User
from app.tasks.service import TaskService
from app.tasks.repository import TaskRepository
from app.tasks.schemas import (
    TaskCreate, TaskUpdate, TaskRead, TaskFilter,
    CategoryCreate, CategoryRead,
    CommentCreate, CommentRead,
)
from app.wallet.service import WalletService
from app.wallet.repository import WalletRepository

router = APIRouter()

task_service = TaskService(
    task_repository=TaskRepository(),
    wallet_service=WalletService(repository=WalletRepository()),
)


@router.get("/categories", response_model=list[CategoryRead])
async def get_categories(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await task_service.get_categories(db)


@router.post("/categories", response_model=CategoryRead)
async def create_category(
    body: CategoryCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await task_service.create_category(db, body, current_user)


@router.delete("/categories/{category_id}", status_code=204)
async def delete_category(
    category_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    await task_service.delete_category(db, category_id, current_user)


@router.post("/", response_model=TaskRead)
async def create_task(
    body: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await task_service.create_task(db, body, current_user)


@router.get("/", response_model=list[TaskRead])
async def get_tasks(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    status: str | None = Query(None),
    creator_id: int | None = Query(None),
    date_from: datetime | None = Query(None),
    date_to: datetime | None = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    filters = TaskFilter(
        status=status,
        creator_id=creator_id,
        date_from=date_from,
        date_to=date_to,
    )
    return await task_service.get_tasks(db, filters, limit, offset)


@router.get("/{task_id}", response_model=TaskRead)
async def get_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await task_service.get_task(db, task_id)


@router.put("/{task_id}", response_model=TaskRead)
async def update_task(
    task_id: int,
    body: TaskUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await task_service.update_task(db, task_id, body, current_user)


@router.delete("/{task_id}", status_code=204)
async def delete_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    await task_service.delete_task(db, task_id, current_user)


@router.post("/{task_id}/assign", response_model=TaskRead)
async def assign_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await task_service.assign_task(db, task_id, current_user)


@router.post("/{task_id}/submit", response_model=TaskRead)
async def submit_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await task_service.submit_task(db, task_id, current_user)


@router.post("/{task_id}/approve", response_model=TaskRead)
async def approve_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await task_service.approve_task(db, task_id, current_user)


@router.post("/{task_id}/reject", response_model=TaskRead)
async def reject_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await task_service.reject_task(db, task_id, current_user)


@router.post("/{task_id}/cancel", response_model=TaskRead)
async def cancel_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await task_service.cancel_task(db, task_id, current_user)


@router.get("/{task_id}/comments", response_model=list[CommentRead])
async def get_comments(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await task_service.get_comments(db, task_id)


@router.post("/{task_id}/comments", response_model=CommentRead)
async def add_comment(
    task_id: int,
    body: CommentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await task_service.add_comment(db, task_id, body, current_user)


@router.delete("/{task_id}/comments/{comment_id}", status_code=204)
async def delete_comment(
    task_id: int,
    comment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    await task_service.delete_comment(db, task_id, comment_id, current_user)