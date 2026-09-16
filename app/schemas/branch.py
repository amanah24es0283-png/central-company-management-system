from uuid import UUID
from pydantic import BaseModel, Field


class BranchCreate(BaseModel):
    company_id: int
    name: str = Field(min_length=2, max_length=150)
    country: str = Field(min_length=2, max_length=100)
    city: str = Field(min_length=2, max_length=100)
    address: str | None = Field(default=None, max_length=255)
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)


class BranchUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=150)
    country: str | None = Field(default=None, min_length=2, max_length=100)
    city: str | None = Field(default=None, min_length=2, max_length=100)
    address: str | None = Field(default=None, max_length=255)
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)
    status: str | None = Field(default=None, pattern="^(active|inactive)$")


class BranchResponse(BaseModel):
    uuid: UUID
    name: str
    country: str
    city: str
    address: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    status: str
