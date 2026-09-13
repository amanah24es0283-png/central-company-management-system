from pydantic import BaseModel, Field


class NotificationCreate(BaseModel):
    user_id: int
    title: str = Field(min_length=2, max_length=200)
    message: str = Field(min_length=2)
    notification_type: str = Field(
        default="general",
        min_length=2,
        max_length=50
    )


class NotificationUpdate(BaseModel):
    is_read: bool
