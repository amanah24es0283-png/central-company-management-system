from datetime import date

from pydantic import BaseModel, Field


class LeaveRequestCreate(BaseModel):
    employee_id: int
    start_date: date
    end_date: date
    reason: str | None = None


class LeaveRequestUpdate(BaseModel):
    start_date: date | None = None
    end_date: date | None = None
    reason: str | None = None


class LeaveRequestStatusUpdate(BaseModel):
    status: str = Field(
        pattern="^(approved|rejected)$"
    )

from uuid import UUID

class LeaveRequestResponse(BaseModel):
    uuid: UUID
    start_date: date
    end_date: date
    reason: str | None = None
    status: str
