from fastapi import Depends, HTTPException, status

from app.core.dependencies import get_current_token


def require_same_branch(
    branch_id: int,
    current_token: dict = Depends(get_current_token),
):
    user_branch_id = current_token.get("branch_id")

    if user_branch_id != branch_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this branch",
        )

    return current_token
