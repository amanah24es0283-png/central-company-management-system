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

def get_employee_performance(
    db: Session,
    company_id: int,
):
    employees = (
        db.query(Employee)
        .join(Department, Employee.department_id == Department.id)
        .join(Branch, Department.branch_id == Branch.id)
        .filter(Branch.company_id == company_id)
        .all()
    )

    performance = []

    for employee in employees:
        task_status_counts = (
            db.query(Task.status, func.count(Task.id))
            .filter(Task.assigned_to == employee.id)
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

        performance.append({
            "employee_id": employee.id,
            "employee_code": employee.employee_code,
            "job_title": employee.job_title,
            "status": employee.status,
            "tasks": {
                "total": total_tasks,
                "pending": task_status.get("pending", 0),
                "in_progress": task_status.get("in_progress", 0),
                "completed": completed_tasks,
                "completion_rate": completion_rate,
            },
        })

    return {
        "company_id": company_id,
        "employees": performance,
    }

def get_employee_distribution_by_branch(
    db: Session,
    company_id: int,
):
    distribution = (
        db.query(
            Branch.id,
            Branch.name,
            func.count(Employee.id),
        )
        .outerjoin(Department, Department.branch_id == Branch.id)
        .outerjoin(Employee, Employee.department_id == Department.id)
        .filter(Branch.company_id == company_id)
        .group_by(Branch.id, Branch.name)
        .order_by(Branch.id)
        .all()
    )

    return {
        "company_id": company_id,
        "branches": [
            {
                "branch_id": branch_id,
                "branch_name": branch_name,
                "employee_count": employee_count,
            }
            for branch_id, branch_name, employee_count in distribution
        ],
    }

def get_leave_analytics(
    db: Session,
    company_id: int,
):
    status_counts = (
        db.query(
            LeaveRequest.status,
            func.count(LeaveRequest.id),
        )
        .join(Employee, LeaveRequest.employee_id == Employee.id)
        .join(Department, Employee.department_id == Department.id)
        .join(Branch, Department.branch_id == Branch.id)
        .filter(Branch.company_id == company_id)
        .group_by(LeaveRequest.status)
        .all()
    )

    status_data = {
        status: count
        for status, count in status_counts
    }

    total = sum(status_data.values())
    approved = status_data.get("approved", 0)
    rejected = status_data.get("rejected", 0)

    approval_rate = (
        round((approved / total) * 100, 2)
        if total
        else 0
    )

    rejection_rate = (
        round((rejected / total) * 100, 2)
        if total
        else 0
    )

    return {
        "company_id": company_id,
        "leave_requests": {
            "total": total,
            "pending": status_data.get("pending", 0),
            "approved": approved,
            "rejected": rejected,
            "approval_rate": approval_rate,
            "rejection_rate": rejection_rate,
        },
    }
