from sqlalchemy.orm import Session

from app.models.employee import Employee
from app.models.task import Task
from app.models.branch import Branch
from app.models.department import Department


def search_all(
    db: Session,
    company_id: int,
    search: str | None = None,
):
    value = f"%{search}%" if search else None

    employees_query = (
        db.query(Employee)
        .join(Department, Employee.department_id == Department.id)
        .join(Branch, Department.branch_id == Branch.id)
        .filter(Branch.company_id == company_id)
    )

    branches_query = (
        db.query(Branch)
        .filter(Branch.company_id == company_id)
    )

    tasks_query = (
        db.query(Task)
        .join(Employee, Task.assigned_to == Employee.id)
        .join(Department, Employee.department_id == Department.id)
        .join(Branch, Department.branch_id == Branch.id)
        .filter(Branch.company_id == company_id)
    )

    if value:
        employees_query = employees_query.filter(
            Employee.employee_code.ilike(value)
            | Employee.job_title.ilike(value)
        )

        branches_query = branches_query.filter(
            Branch.name.ilike(value)
            | Branch.city.ilike(value)
            | Branch.address.ilike(value)
        )

        tasks_query = tasks_query.filter(
            Task.title.ilike(value)
            | Task.description.ilike(value)
        )

    employees = employees_query.order_by(Employee.id).all()
    branches = branches_query.order_by(Branch.id).all()
    tasks = tasks_query.order_by(Task.id).all()

    return {
        "company_id": company_id,
        "search": search,
        "employees": [
            {
                "id": employee.id,
                "employee_code": employee.employee_code,
                "job_title": employee.job_title,
                "status": employee.status,
            }
            for employee in employees
        ],
        "branches": [
            {
                "id": branch.id,
                "name": branch.name,
                "country": branch.country,
                "city": branch.city,
                "status": branch.status,
            }
            for branch in branches
        ],
        "tasks": [
            {
                "id": task.id,
                "title": task.title,
                "priority": task.priority,
                "status": task.status,
            }
            for task in tasks
        ],
    }
