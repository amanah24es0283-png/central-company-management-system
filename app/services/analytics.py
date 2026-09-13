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

    tasks = (
        db.query(Task)
        .join(Employee, Task.assigned_to == Employee.id)
        .join(Department, Employee.department_id == Department.id)
        .join(Branch, Department.branch_id == Branch.id)
        .filter(Branch.company_id == company_id)
        .count()
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
            "tasks": tasks,
            "leave_requests": leave_requests,
        }
    }
