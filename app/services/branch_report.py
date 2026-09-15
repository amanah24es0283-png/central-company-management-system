from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.branch import Branch
from app.models.department import Department
from app.models.employee import Employee


def get_branch_report(
    db: Session,
    company_id: int,
):
    branches = (
        db.query(
            Branch,
            func.count(func.distinct(Department.id)).label("department_count"),
            func.count(func.distinct(Employee.id)).label("employee_count"),
        )
        .outerjoin(Department, Department.branch_id == Branch.id)
        .outerjoin(Employee, Employee.department_id == Department.id)
        .filter(Branch.company_id == company_id)
        .group_by(Branch.id)
        .order_by(Branch.id)
        .all()
    )

    return {
        "company_id": company_id,
        "count": len(branches),
        "branches": [
            {
                "branch_id": branch.id,
                "name": branch.name,
                "country": branch.country,
                "city": branch.city,
                "address": branch.address,
                "latitude": branch.latitude,
                "longitude": branch.longitude,
                "status": branch.status,
                "department_count": department_count,
                "employee_count": employee_count,
            }
            for branch, department_count, employee_count in branches
        ],
    }
