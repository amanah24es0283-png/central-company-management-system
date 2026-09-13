from datetime import datetime

from pydantic import BaseModel, Field


class AttendanceCreate(BaseModel):
    employee_id: int
    check_in: datetime | None = None
    note: str | None = None


class AttendanceUpdate(BaseModel):
    check_in: datetime | None = None
    check_out: datetime | None = None
    status: str | None = Field(
        default=None,
        pattern="^(present|absent|late|leave)$"
    )
    note: str | None = None
