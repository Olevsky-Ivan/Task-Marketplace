from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task
from app.models.comment import Comment
from app.models.user import User, UserRole
from app.tasks.repository import TaskRepository
from app.tasks.schemas import TaskCreate, TaskUpdate, TaskFilter, CategoryCreate, CommentCreate
from app.wallet.service import WalletService


class TaskService:

    def __init__(self, task_repository: TaskRepository, wallet_service: WalletService):
        self.repository = task_repository
        self.wallet_service = wallet_service

    async def create_task(self, db: AsyncSession, data: TaskCreate, current_user: User) -> Task:
        if current_user.role not in (UserRole.CUSTOMER, UserRole.ADMIN):
            raise HTTPException(status_code=403, detail="Only customers can create tasks")

        if data.category_id is not None:
            category = await self.repository.get_category_by_id(db, data.category_id)
            if not category:
                raise HTTPException(status_code=404, detail="Category not found")

        await self.wallet_service.freeze(db, current_user.id, Decimal(str(data.reward)))

        task = Task(
            title=data.title,
            description=data.description,
            reward=Decimal(str(data.reward)),
            creator_id=current_user.id,
            category_id=data.category_id,
            status="open",
        )

        await self.repository.create(db, task)
        await db.commit()
        await db.refresh(task)
        return task

    async def get_task(self, db: AsyncSession, task_id: int) -> Task:
        task = await self.repository.get_by_id(db, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task

    async def get_tasks(
        self,
        db: AsyncSession,
        filters: TaskFilter,
        limit: int,
        offset: int,
    ) -> list[Task]:
        return await self.repository.get_all_filtered(db, filters, limit, offset)

    async def update_task(
        self,
        db: AsyncSession,
        task_id: int,
        data: TaskUpdate,
        current_user: User,
    ) -> Task:
        task = await self.get_task(db, task_id)

        if task.creator_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not your task")
        if task.status != "open":
            raise HTTPException(status_code=400, detail="Can only edit open tasks")

        result = await self.repository.update(db, task, data)
        await db.commit()
        return result

    async def delete_task(self, db: AsyncSession, task_id: int, current_user: User) -> None:
        task = await self.get_task(db, task_id)

        if task.creator_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not your task")
        if task.status != "open":
            raise HTTPException(status_code=400, detail="Can only delete open tasks")

        await self.wallet_service.unfreeze_on_cancel(db, current_user.id, task.reward)
        await self.repository.delete(db, task)
        await db.commit()

    async def assign_task(self, db: AsyncSession, task_id: int, current_user: User) -> Task:
        if current_user.role != UserRole.EXECUTOR:
            raise HTTPException(status_code=403, detail="Only executors can take tasks")

        task = await self.get_task(db, task_id)

        if task.status != "open":
            raise HTTPException(status_code=400, detail="Task is not available")
        if task.executor_id is not None:
            raise HTTPException(status_code=400, detail="Task already assigned")

        result = await self.repository.set_executor(db, task, current_user.id)
        await db.commit()
        return result

    async def submit_task(self, db: AsyncSession, task_id: int, current_user: User) -> Task:
        task = await self.get_task(db, task_id)

        if task.executor_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not your task")
        if task.status != "in_progress":
            raise HTTPException(status_code=400, detail="Task is not in progress")

        result = await self.repository.set_status(db, task, "submitted")
        await db.commit()
        return result

    async def approve_task(self, db: AsyncSession, task_id: int, current_user: User) -> Task:
        task = await self.get_task(db, task_id)

        if task.creator_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not your task")
        if task.status != "submitted":
            raise HTTPException(status_code=400, detail="Task is not submitted yet")

        await self.wallet_service.transfer_on_approve(
            db,
            task_id=task.id,
            customer_id=task.creator_id,
            executor_id=task.executor_id,
            amount=task.reward,
        )

        result = await self.repository.set_status(db, task, "approved")
        await db.commit()
        return result

    async def reject_task(self, db: AsyncSession, task_id: int, current_user: User) -> Task:
        task = await self.get_task(db, task_id)

        if task.creator_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not your task")
        if task.status != "submitted":
            raise HTTPException(status_code=400, detail="Task is not submitted")

        result = await self.repository.set_status(db, task, "in_progress")
        await db.commit()
        return result

    async def cancel_task(self, db: AsyncSession, task_id: int, current_user: User) -> Task:
        task = await self.get_task(db, task_id)

        if task.creator_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not your task")
        if task.status in ("approved", "cancelled"):
            raise HTTPException(status_code=400, detail="Cannot cancel this task")

        if task.status in ("open", "in_progress", "submitted"):
            await self.wallet_service.unfreeze_on_cancel(db, current_user.id, task.reward)

        result = await self.repository.set_status(db, task, "cancelled")
        await db.commit()
        return result


    async def get_categories(self, db: AsyncSession) -> list:
        return await self.repository.get_all_categories(db)

    async def create_category(self, db: AsyncSession, data: CategoryCreate, current_user: User):
        if current_user.role != UserRole.ADMIN:
            raise HTTPException(status_code=403, detail="Only admin can manage categories")
        category = await self.repository.create_category(db, data.name)
        await db.commit()
        return category

    async def delete_category(self, db: AsyncSession, category_id: int, current_user: User):
        if current_user.role != UserRole.ADMIN:
            raise HTTPException(status_code=403, detail="Only admin can manage categories")
        category = await self.repository.get_category_by_id(db, category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        await self.repository.delete_category(db, category)
        await db.commit()


    async def get_comments(self, db: AsyncSession, task_id: int) -> list:
        await self.get_task(db, task_id)
        return await self.repository.get_comments(db, task_id)

    async def add_comment(
        self,
        db: AsyncSession,
        task_id: int,
        data: CommentCreate,
        current_user: User,
    ) -> Comment:
        await self.get_task(db, task_id)
        comment = await self.repository.create_comment(db, task_id, current_user.id, data.text)
        await db.commit()
        await db.refresh(comment)
        return comment

    async def delete_comment(
        self,
        db: AsyncSession,
        task_id: int,
        comment_id: int,
        current_user: User,
    ) -> None:
        await self.get_task(db, task_id)
        comment = await self.repository.get_comment_by_id(db, comment_id)

        if not comment:
            raise HTTPException(status_code=404, detail="Comment not found")
        if comment.task_id != task_id:
            raise HTTPException(status_code=400, detail="Comment does not belong to this task")
        if comment.user_id != current_user.id and current_user.role != UserRole.ADMIN:
            raise HTTPException(status_code=403, detail="Not your comment")

        await self.repository.delete_comment(db, comment)
        await db.commit()