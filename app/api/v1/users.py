from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.authorization import require_roles
from app.core.security import hash_password
from app.db.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])




@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    data: UserCreate,
    current_token: dict = Depends(require_roles("OWNER")),
    db: Session = Depends(get_db),
):
    if data.company_id != current_token["company_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot create a user for another company",
        )

    existing_user = db.query(User).filter(User.email == data.email).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    user = User(
        full_name=data.full_name,
        email=data.email,
        password_hash=hash_password(data.password),
        role=data.role,
        status=data.status,
        company_id=data.company_id,
        branch_id=data.branch_id,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@router.get("/", response_model=list[UserResponse])
def list_users(
    current_token: dict = Depends(require_roles("OWNER")),
    db: Session = Depends(get_db),
):
    users = (
        db.query(User)
        .filter(User.company_id == current_token["company_id"])
        .all()
    )
    return users


@router.get("/{user_uuid}", response_model=UserResponse)
def get_user(
    user_uuid: UUID,
    current_token: dict = Depends(require_roles("OWNER")),
    db: Session = Depends(get_db),
):
    user = (
        db.query(User)
        .filter(
            User.uuid == user_uuid,
            User.company_id == current_token["company_id"],
        )
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user


@router.patch("/{user_uuid}", response_model=UserResponse)
def update_user(
    user_uuid: UUID,
    data: UserUpdate,
    current_token: dict = Depends(require_roles("OWNER")),
    db: Session = Depends(get_db),
):
    user = (
        db.query(User)
        .filter(
            User.uuid == user_uuid,
            User.company_id == current_token["company_id"],
        )
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)

    return user
