from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.task import Task
from app.models.category import Category
from app.models.comment import Comment
from app.models.tag import Tag
from app.tasks.schemas import TaskFilter


class TaskRepository:

    async def create(self, db: AsyncSession, task: Task) -> Task:
        db.add(task)
        await db.flush()
        await db.refresh(task)
        return task

    async def get_by_id(self, db: AsyncSession, task_id: int) -> Task | None:
        return await db.get(Task, task_id)

    async def get_all_filtered(
        self,
        db: AsyncSession,
        filters: TaskFilter,
        limit: int,
        offset: int,
    ) -> list[Task]:
        query = select(Task)

        if filters.status is not None:
            query = query.where(Task.status == filters.status)
        if filters.creator_id is not None:
            query = query.where(Task.creator_id == filters.creator_id)
        if filters.date_from is not None:
            query = query.where(Task.created_at >= filters.date_from)
        if filters.date_to is not None:
            query = query.where(Task.created_at <= filters.date_to)

        query = query.limit(limit).offset(offset)
        result = await db.execute(query)
        return result.scalars().all()

    async def update(self, db: AsyncSession, task: Task, data) -> Task:
        if data.title is not None:
            task.title = data.title
        if data.description is not None:
            task.description = data.description
        await db.flush()
        await db.refresh(task)
        return task

    async def delete(self, db: AsyncSession, task: Task) -> None:
        await db.delete(task)
        await db.flush()

    async def set_executor(self, db: AsyncSession, task: Task, executor_id: int) -> Task:
        task.executor_id = executor_id
        task.status = "in_progress"
        await db.flush()
        await db.refresh(task)
        return task

    async def set_status(self, db: AsyncSession, task: Task, status: str) -> Task:
        task.status = status
        await db.flush()
        await db.refresh(task)
        return task

    async def get_tags_by_ids(self, db: AsyncSession, tag_ids: list[int]) -> list[Tag]:
        result = await db.execute(select(Tag).where(Tag.id.in_(tag_ids)))
        return result.scalars().all()

    async def get_all_tags(self, db: AsyncSession) -> list[Tag]:
        result = await db.execute(select(Tag))
        return result.scalars().all()

    async def create_tag(self, db: AsyncSession, name: str) -> Tag:
        tag = Tag(name=name)
        db.add(tag)
        await db.flush()
        await db.refresh(tag)
        return tag

    async def delete_tag(self, db: AsyncSession, tag: Tag) -> None:
        await db.delete(tag)
        await db.flush()

    async def get_tag_by_id(self, db: AsyncSession, tag_id: int) -> Tag | None:
        return await db.get(Tag, tag_id)

    async def get_all_categories(self, db: AsyncSession) -> list[Category]:
        result = await db.execute(select(Category))
        return result.scalars().all()

    async def get_category_by_id(self, db: AsyncSession, category_id: int) -> Category | None:
        return await db.get(Category, category_id)

    async def create_category(self, db: AsyncSession, name: str) -> Category:
        category = Category(name=name)
        db.add(category)
        await db.flush()
        await db.refresh(category)
        return category

    async def delete_category(self, db: AsyncSession, category: Category) -> None:
        await db.delete(category)
        await db.flush()

    async def get_comments(self, db: AsyncSession, task_id: int) -> list[Comment]:
        result = await db.execute(
            select(Comment).where(Comment.task_id == task_id).order_by(Comment.created_at.asc())
        )
        return result.scalars().all()

    async def create_comment(self, db: AsyncSession, task_id: int, user_id: int, text: str) -> Comment:
        comment = Comment(task_id=task_id, user_id=user_id, text=text)
        db.add(comment)
        await db.flush()
        await db.refresh(comment)
        return comment

    async def get_comment_by_id(self, db: AsyncSession, comment_id: int) -> Comment | None:
        return await db.get(Comment, comment_id)

    async def delete_comment(self, db: AsyncSession, comment: Comment) -> None:
        await db.delete(comment)
        await db.flush()