from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.jwt import create_access_token
from app.core.dependencies import get_current_token
from app.core.security import verify_password
from app.db.database import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/login")
def login(
    data: LoginRequest,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == data.email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    if user.status != "active":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )

    access_token = create_access_token(
        data={
            "user_id": user.id,
            "role": user.role,
            "company_id": user.company_id,
            "branch_id": user.branch_id,
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "role": user.role,
            "status": user.status,
            "company_id": user.company_id,
            "branch_id": user.branch_id,
        },
    }


@router.get("/me")
def get_me(current_token: dict = Depends(get_current_token)):
    return {
        "message": "Authentication successful",
        "user_id": current_token["user_id"],
        "role": current_token["role"],
        "company_id": current_token["company_id"],
        "branch_id": current_token["branch_id"],
    }
