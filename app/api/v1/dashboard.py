from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_token
from app.db.database import get_db

from app.models.company import Company
from app.models.branch import Branch
from app.models.department import Department
from app.models.employee import Employee
from app.models.task import Task
from app.models.leave_request import LeaveRequest
from app.models.report import Report
from app.models.notification import Notification
from app.models.user import User

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get("/")
def get_dashboard(
    current_token: dict = Depends(get_current_token),
    db: Session = Depends(get_db),
):
    company_id = current_token["company_id"]

    companies_count = db.query(Company).filter(
        Company.id == company_id
    ).count()

    branches_count = db.query(Branch).filter(
        Branch.company_id == company_id
    ).count()

    employees_count = (
        db.query(Employee)
        .join(Department, Employee.department_id == Department.id)
        .join(Branch, Department.branch_id == Branch.id)
        .filter(Branch.company_id == company_id)
        .count()
    )

    tasks_query = (
        db.query(Task)
        .join(Employee, Task.assigned_to == Employee.id)
        .join(Department, Employee.department_id == Department.id)
        .join(Branch, Department.branch_id == Branch.id)
        .filter(Branch.company_id == company_id)
    )

    tasks_count = tasks_query.count()

    tasks_pending = tasks_query.filter(
        Task.status == "pending"
    ).count()

    tasks_in_progress = tasks_query.filter(
        Task.status == "in_progress"
    ).count()

    tasks_completed = tasks_query.filter(
        Task.status == "completed"
    ).count()

    leave_query = (
        db.query(LeaveRequest)
        .join(Employee, LeaveRequest.employee_id == Employee.id)
        .join(Department, Employee.department_id == Department.id)
        .join(Branch, Department.branch_id == Branch.id)
        .filter(Branch.company_id == company_id)
    )

    leave_pending = leave_query.filter(
        LeaveRequest.status == "pending"
    ).count()

    leave_approved = leave_query.filter(
        LeaveRequest.status == "approved"
    ).count()

    leave_rejected = leave_query.filter(
        LeaveRequest.status == "rejected"
    ).count()

    reports_count = db.query(Report).filter(
        Report.company_id == company_id
    ).count()

    notifications_unread = (
        db.query(Notification)
        .join(User, Notification.user_id == User.id)
        .filter(
            User.company_id == company_id,
            Notification.is_read == False,
        )
        .count()
    )

    return {
        "company_id": company_id,
        "summary": {
            "companies": companies_count,
            "branches": branches_count,
            "employees": employees_count,
            "tasks": tasks_count,
            "reports": reports_count,
        },
        "tasks": {
            "pending": tasks_pending,
            "in_progress": tasks_in_progress,
            "completed": tasks_completed,
        },
        "leave_requests": {
            "pending": leave_pending,
            "approved": leave_approved,
            "rejected": leave_rejected,
        },
        "notifications": {
            "unread": notifications_unread,
        },
    }
