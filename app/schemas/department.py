from pydantic import BaseModel, Field


class DepartmentCreate(BaseModel):
    branch_id: int
    name: str = Field(min_length=2, max_length=150)
    description: str | None = None
    manager_id: int | None = None


class DepartmentUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=150)
    description: str | None = None
    manager_id: int | None = None
