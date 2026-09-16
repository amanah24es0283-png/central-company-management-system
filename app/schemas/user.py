from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    full_name: str = Field(min_length=2, max_length=150)
    email: EmailStr
    password: str = Field(min_length=8, max_length=100)
    role: str = Field(default="EMPLOYEE", min_length=2, max_length=30)
    status: str = Field(default="active", pattern="^(active|inactive)$")
    company_id: int
    branch_id: int | None = None


class UserUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=2, max_length=150)
    email: EmailStr | None = None
    role: str | None = Field(default=None, min_length=2, max_length=30)
    status: str | None = Field(default=None, pattern="^(active|inactive)$")
    company_id: int | None = None
    branch_id: int | None = None


class UserResponse(BaseModel):
    uuid: UUID
    full_name: str
    email: EmailStr
    role: str
    status: str
    company_id: int
    branch_id: int | None = None
    created_at: datetime
    updated_at: datetime
