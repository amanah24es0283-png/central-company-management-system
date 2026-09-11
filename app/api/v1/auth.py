from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.jwt import create_access_token
from app.core.dependencies import get_current_token
from app.core.authorization import require_roles
from app.core.tenant import require_same_company
from app.core.branch_access import require_same_branch
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
def get_me(current_token: dict = Depends(require_roles("OWNER"))):
    return {
        "message": "Authentication successful",
        "user_id": current_token["user_id"],
        "role": current_token["role"],
        "company_id": current_token["company_id"],
        "branch_id": current_token["branch_id"],
    }


@router.get("/company/{company_id}/access")
def check_company_access(
    company_id: int,
    current_token: dict = Depends(require_same_company),
):
    return {
        "message": "Company access granted",
        "company_id": company_id,
        "user_company_id": current_token["company_id"],
    }


@router.get("/branch/{branch_id}/access")
def check_branch_access(
    branch_id: int,
    current_token: dict = Depends(require_same_branch),
):
    return {
        "message": "Branch access granted",
        "branch_id": branch_id,
        "user_branch_id": current_token["branch_id"],
    }
