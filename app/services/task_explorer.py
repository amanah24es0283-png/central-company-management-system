from sqlalchemy.orm import Session

from app.models.task import Task
from app.models.employee import Employee
from app.models.department import Department
from app.models.branch import Branch


def search_tasks(
    db: Session,
    company_id: int,
    search: str | None = None,
    status: str | None = None,
    priority: str | None = None,
    employee_id: int | None = None,
):
    query = (
        db.query(Task)
        .join(Employee, Task.assigned_to == Employee.id)
        .join(Department, Employee.department_id == Department.id)
        .join(Branch, Department.branch_id == Branch.id)
        .filter(Branch.company_id == company_id)
    )

    if status:
        query = query.filter(Task.status == status)

    if priority:
        query = query.filter(Task.priority == priority)

    if employee_id is not None:
        query = query.filter(Task.assigned_to == employee_id)

    if search:
        search_value = f"%{search}%"
        query = query.filter(
            Task.title.ilike(search_value)
            | Task.description.ilike(search_value)
        )

    return query.order_by(Task.id).all()
