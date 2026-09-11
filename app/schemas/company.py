from pydantic import BaseModel, Field


class CompanyCreate(BaseModel):
    name: str = Field(min_length=2, max_length=150)
    description: str | None = None
    country: str = Field(min_length=2, max_length=100)


class CompanyUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=150)
    description: str | None = None
    country: str | None = Field(default=None, min_length=2, max_length=100)
    status: str | None = Field(default=None, pattern="^(active|inactive)$")
