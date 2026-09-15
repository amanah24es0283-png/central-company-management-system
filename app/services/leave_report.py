from sqlalchemy.orm import Session

from app.models.leave_request import LeaveRequest
from app.models.employee import Employee
from app.models.department import Department
from app.models.branch import Branch


def get_leave_report(
    db: Session,
    company_id: int,
):
    requests = (
        db.query(
            LeaveRequest,
            Employee.employee_code.label("employee_code"),
            Department.name.label("department_name"),
            Branch.id.label("branch_id"),
            Branch.name.label("branch_name"),
        )
        .join(Employee, LeaveRequest.employee_id == Employee.id)
        .join(Department, Employee.department_id == Department.id)
        .join(Branch, Department.branch_id == Branch.id)
        .filter(Branch.company_id == company_id)
        .order_by(LeaveRequest.id)
        .all()
    )

    return {
        "company_id": company_id,
        "count": len(requests),
        "leave_requests": [
            {
                "leave_request_id": request.id,
                "employee_id": request.employee_id,
                "employee_code": employee_code,
                "start_date": request.start_date,
                "end_date": request.end_date,
                "reason": request.reason,
                "status": request.status,
                "approved_by": request.approved_by,
                "department_name": department_name,
                "branch_id": branch_id,
                "branch_name": branch_name,
            }
            for request, employee_code, department_name, branch_id, branch_name in requests
        ],
    }
