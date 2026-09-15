from sqlalchemy.orm import Session

from app.models.task import Task
from app.models.employee import Employee
from app.models.department import Department
from app.models.branch import Branch


def get_task_report(
    db: Session,
    company_id: int,
):
    tasks = (
        db.query(
            Task,
            Employee.employee_code.label("employee_code"),
            Department.id.label("department_id"),
            Department.name.label("department_name"),
            Branch.id.label("branch_id"),
            Branch.name.label("branch_name"),
        )
        .join(Employee, Task.assigned_to == Employee.id)
        .join(Department, Employee.department_id == Department.id)
        .join(Branch, Department.branch_id == Branch.id)
        .filter(Branch.company_id == company_id)
        .order_by(Task.id)
        .all()
    )

    return {
        "company_id": company_id,
        "count": len(tasks),
        "tasks": [
            {
                "task_id": task.id,
                "title": task.title,
                "description": task.description,
                "priority": task.priority,
                "status": task.status,
                "employee_id": task.assigned_to,
                "employee_code": employee_code,
                "department_id": department_id,
                "department_name": department_name,
                "branch_id": branch_id,
                "branch_name": branch_name,
            }
            for task, employee_code, department_id, department_name, branch_id, branch_name in tasks
        ],
    }
