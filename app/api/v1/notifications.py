from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_token
from app.core.authorization import require_roles
from app.db.database import get_db
from app.models.notification import Notification
from app.models.user import User
from app.schemas.notification import (
    NotificationCreate,
    NotificationUpdate,
)

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_notification(
    data: NotificationCreate,
    current_token: dict = Depends(require_roles("OWNER")),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(
        User.id == data.user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if user.company_id != current_token["company_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot create a notification for another company's user",
        )

    notification = Notification(
        user_id=data.user_id,
        title=data.title,
        message=data.message,
        notification_type=data.notification_type,
        is_read=False,
    )

    db.add(notification)
    db.commit()
    db.refresh(notification)

    return notification


@router.get("/")
def list_notifications(
    unread_only: bool = False,
    current_token: dict = Depends(get_current_token),
    db: Session = Depends(get_db),
):
    query = db.query(Notification).filter(
        Notification.user_id == current_token["user_id"]
    )

    if unread_only:
        query = query.filter(
            Notification.is_read == False
        )

    return query.all()


@router.get("/{notification_id}")
def get_notification(
    notification_id: int,
    current_token: dict = Depends(get_current_token),
    db: Session = Depends(get_db),
):
    notification = db.query(Notification).filter(
        Notification.id == notification_id
    ).first()

    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found",
        )

    if notification.user_id != current_token["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this notification",
        )

    return notification


@router.patch("/{notification_id}")
def update_notification(
    notification_id: int,
    data: NotificationUpdate,
    current_token: dict = Depends(get_current_token),
    db: Session = Depends(get_db),
):
    notification = db.query(Notification).filter(
        Notification.id == notification_id
    ).first()

    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found",
        )

    if notification.user_id != current_token["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this notification",
        )

    notification.is_read = data.is_read

    db.commit()
    db.refresh(notification)

    return notification
