from datetime import datetime

from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    title: str = Field(min_length=2, max_length=200)
    description: str | None = None
    assigned_to: int
    priority: str = Field(
        default="medium",
        pattern="^(low|medium|high|urgent)$"
    )
    due_date: datetime | None = None


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=200)
    description: str | None = None
    assigned_to: int | None = None
    priority: str | None = Field(
        default=None,
        pattern="^(low|medium|high|urgent)$"
    )
    status: str | None = Field(
        default=None,
        pattern="^(pending|in_progress|completed|cancelled)$"
    )
    due_date: datetime | None = None


class TaskStatusUpdate(BaseModel):
    status: str = Field(
        pattern="^(pending|in_progress|completed|cancelled)$"
    )
    note: str | None = None
