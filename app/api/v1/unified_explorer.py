from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.authorization import require_roles
from app.db.database import get_db
from app.services.unified_explorer import search_all


router = APIRouter(
    prefix="/unified-explorer",
    tags=["Unified Data Explorer"],
)


@router.get("/search")
def unified_search(
    search: str | None = Query(default=None),
    current_token: dict = Depends(require_roles("OWNER")),
    db: Session = Depends(get_db),
):
    company_id = current_token["company_id"]

    return search_all(
        db=db,
        company_id=company_id,
        search=search,
    )
