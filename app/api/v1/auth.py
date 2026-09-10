from fastapi import APIRouter

from app.schemas.auth import LoginRequest

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/login")
def login(data: LoginRequest):
    return {
        "message": "Login data received",
        "email": data.email,
    }
