from datetime import datetime

from pydantic import BaseModel, Field


class EmployeeCreate(BaseModel):
    user_id: int
    department_id: int
    employee_code: str = Field(min_length=2, max_length=50)
    job_title: str = Field(min_length=2, max_length=150)
    phone: str | None = Field(default=None, max_length=30)
    hire_date: datetime | None = None


class EmployeeUpdate(BaseModel):
    department_id: int | None = None
    employee_code: str | None = Field(default=None, min_length=2, max_length=50)
    job_title: str | None = Field(default=None, min_length=2, max_length=150)
    phone: str | None = Field(default=None, max_length=30)
    hire_date: datetime | None = None
    status: str | None = Field(default=None, pattern="^(active|inactive)$")

from uuid import UUID

class EmployeeResponse(BaseModel):
    uuid: UUID
    employee_code: str
    job_title: str
    status: str
