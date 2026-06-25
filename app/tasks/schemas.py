from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from enum import Enum

class CategoryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str


class CategoryCreate(BaseModel):
    name: str



class TaskStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    SUBMITTED = "submitted"
    APPROVED = "approved"
    CANCELLED = "cancelled"


class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    reward: float  # amount being frozen
    category_id: int | None = None


class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None


class TaskRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    status: TaskStatus
    reward: float
    creator_id: int
    executor_id: int | None
    created_at: datetime
    category_id: int | None
    category: CategoryRead | None

class TaskFilter(BaseModel):
    status: TaskStatus | None = None
    creator_id: int | None = None
    date_from: datetime | None = None
    date_to: datetime | None = None


class CommentCreate(BaseModel):
    text: str


class CommentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    text: str
    user_id: int
    task_id: int
    created_at: datetime