from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.authorization import require_roles
from app.db.database import get_db
from app.services.analytics import get_company_analytics


router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)


@router.get("/company")
def company_analytics(
    current_token: dict = Depends(require_roles("OWNER")),
    db: Session = Depends(get_db),
):
    company_id = current_token["company_id"]

    return get_company_analytics(
        db=db,
        company_id=company_id,
    )
