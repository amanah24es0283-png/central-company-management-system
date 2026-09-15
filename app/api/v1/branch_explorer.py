from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.authorization import require_roles
from app.db.database import get_db
from app.services.branch_explorer import search_branches


router = APIRouter(
    prefix="/branch-explorer",
    tags=["Branch Explorer"],
)


@router.get("/branches")
def explore_branches(
    search: str | None = Query(default=None),
    country: str | None = Query(default=None),
    city: str | None = Query(default=None),
    status: str | None = Query(default=None),
    current_token: dict = Depends(require_roles("OWNER")),
    db: Session = Depends(get_db),
):
    company_id = current_token["company_id"]

    branches = search_branches(
        db=db,
        company_id=company_id,
        search=search,
        country=country,
        city=city,
        status=status,
    )

    return {
        "company_id": company_id,
        "count": len(branches),
        "branches": [
            {
                "id": branch.id,
                "name": branch.name,
                "country": branch.country,
                "city": branch.city,
                "address": branch.address,
                "latitude": branch.latitude,
                "longitude": branch.longitude,
                "status": branch.status,
            }
            for branch in branches
        ],
    }
