from sqlalchemy.orm import Session

from app.models.employee import Employee
from app.models.department import Department
from app.models.branch import Branch


def search_employees(
    db: Session,
    company_id: int,
    search: str | None = None,
    branch_id: int | None = None,
    department_id: int | None = None,
    status: str | None = None,
):
    query = (
        db.query(Employee)
        .join(Department, Employee.department_id == Department.id)
        .join(Branch, Department.branch_id == Branch.id)
        .filter(Branch.company_id == company_id)
    )

    if branch_id is not None:
        query = query.filter(Branch.id == branch_id)

    if department_id is not None:
        query = query.filter(Department.id == department_id)

    if status:
        query = query.filter(Employee.status == status)

    if search:
        search_value = f"%{search}%"

        query = query.filter(
            Employee.employee_code.ilike(search_value)
            | Employee.job_title.ilike(search_value)
        )

    return query.order_by(Employee.id).all()
