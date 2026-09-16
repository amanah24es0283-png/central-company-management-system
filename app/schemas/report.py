from pydantic import BaseModel, Field


class ReportCreate(BaseModel):
    branch_id: int | None = None
    report_type: str = Field(min_length=2, max_length=50)
    title: str = Field(min_length=2, max_length=200)
    content: str | None = None


class ReportUpdate(BaseModel):
    branch_id: int | None = None
    report_type: str | None = Field(
        default=None,
        min_length=2,
        max_length=50
    )
    title: str | None = Field(
        default=None,
        min_length=2,
        max_length=200
    )
    content: str | None = None


class ReportStatusUpdate(BaseModel):
    status: str = Field(
        pattern="^(draft|submitted|approved|rejected)$"
    )

from uuid import UUID

class ReportResponse(BaseModel):
    uuid: UUID
    report_type: str
    title: str
    content: str | None = None
    status: str
