from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.company import Company
from app.models.branch import Branch
from app.models.department import Department
from app.models.employee import Employee
from app.models.task import Task
from app.models.leave_request import LeaveRequest


def get_company_analytics(db: Session, company_id: int):
    companies = db.query(Company).filter(
        Company.id == company_id
    ).count()

    branches = db.query(Branch).filter(
        Branch.company_id == company_id
    ).count()

    employees = (
        db.query(Employee)
        .join(Department, Employee.department_id == Department.id)
        .join(Branch, Department.branch_id == Branch.id)
        .filter(Branch.company_id == company_id)
        .count()
    )

    employee_status_counts = (
        db.query(Employee.status, func.count(Employee.id))
        .join(Department, Employee.department_id == Department.id)
        .join(Branch, Department.branch_id == Branch.id)
        .filter(Branch.company_id == company_id)
        .group_by(Employee.status)
        .all()
    )

    employee_status = {
        status: count
        for status, count in employee_status_counts
    }

    tasks = (
        db.query(Task)
        .join(Employee, Task.assigned_to == Employee.id)
        .join(Department, Employee.department_id == Department.id)
        .join(Branch, Department.branch_id == Branch.id)
        .filter(Branch.company_id == company_id)
        .count()
    )

    task_status_counts = (
        db.query(Task.status, func.count(Task.id))
        .join(Employee, Task.assigned_to == Employee.id)
        .join(Department, Employee.department_id == Department.id)
        .join(Branch, Department.branch_id == Branch.id)
        .filter(Branch.company_id == company_id)
        .group_by(Task.status)
        .all()
    )

    task_status = {
        status: count
        for status, count in task_status_counts
    }

    total_tasks = sum(task_status.values())
    completed_tasks = task_status.get("completed", 0)

    completion_rate = (
        round((completed_tasks / total_tasks) * 100, 2)
        if total_tasks
        else 0
    )

    leave_requests = (
        db.query(LeaveRequest)
        .join(Employee, LeaveRequest.employee_id == Employee.id)
        .join(Department, Employee.department_id == Department.id)
        .join(Branch, Department.branch_id == Branch.id)
        .filter(Branch.company_id == company_id)
        .count()
    )

    return {
        "company_id": company_id,
        "summary": {
            "companies": companies,
            "branches": branches,
            "employees": employees,
            "employee_status": {
                "active": employee_status.get("active", 0),
                "inactive": employee_status.get("inactive", 0),
                "total": employees,
            },
            "tasks": tasks,
            "task_status": {
                "pending": task_status.get("pending", 0),
                "in_progress": task_status.get("in_progress", 0),
                "completed": task_status.get("completed", 0),
                "total": total_tasks,
                "completion_rate": completion_rate,
            },
            "leave_requests": leave_requests,
        }
    }
