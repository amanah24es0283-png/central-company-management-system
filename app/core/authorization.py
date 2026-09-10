from fastapi import Depends, HTTPException, status

from app.core.dependencies import get_current_token


def require_roles(*allowed_roles: str):
    def role_checker(
        current_token: dict = Depends(get_current_token),
    ):
        user_role = current_token.get("role")

        if user_role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource",
            )

        return current_token

    return role_checker
