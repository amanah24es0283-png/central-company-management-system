from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.authorization import require_roles
from app.db.database import get_db
from app.services.data_explorer import search_employees

router = APIRouter(
    prefix="/data-explorer",
    tags=["Data Explorer"],
)


@router.get("/employees")
def explore_employees(
    search: str | None = Query(default=None),
    branch_id: int | None = Query(default=None),
    current_token: dict = Depends(require_roles("OWNER")),
    db: Session = Depends(get_db),
):
    company_id = current_token["company_id"]

    employees = search_employees(
        db=db,
        company_id=company_id,
        search=search,
        branch_id=branch_id,
    )

    return {
        "company_id": company_id,
        "count": len(employees),
        "employees": [
            {
                "id": employee.id,
                "employee_code": employee.employee_code,
                "job_title": employee.job_title,
                "status": employee.status,
            }
            for employee in employees
        ],
    }
