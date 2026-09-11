from fastapi import Depends, HTTPException, status

from app.core.dependencies import get_current_token


def require_same_company(
    company_id: int,
    current_token: dict = Depends(get_current_token),
):
    user_company_id = current_token.get("company_id")

    if user_company_id != company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this company",
        )

    return current_token
