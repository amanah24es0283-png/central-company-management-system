from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.authorization import require_roles
from app.db.database import get_db
from app.models.leave_request import LeaveRequest
from app.services.audit import log_action
from app.models.employee import Employee
from app.models.department import Department
from app.models.branch import Branch
from app.schemas.leave_request import (
    LeaveRequestCreate,
    LeaveRequestUpdate,
    LeaveRequestStatusUpdate,
)

router = APIRouter(
    prefix="/leave-requests",
    tags=["Leave Requests"],
)


def get_employee_company(employee_id: int, db: Session):
    employee = db.query(Employee).filter(
        Employee.id == employee_id
    ).first()

    if not employee:
        return None, None, None

    department = db.query(Department).filter(
        Department.id == employee.department_id
    ).first()

    if not department:
        return employee, None, None

    branch = db.query(Branch).filter(
        Branch.id == department.branch_id
    ).first()

    return employee, department, branch


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_leave_request(
    data: LeaveRequestCreate,
    current_token: dict = Depends(require_roles("OWNER")),
    db: Session = Depends(get_db),
):
    if data.end_date < data.start_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="End date cannot be before start date",
        )

    employee, department, branch = get_employee_company(
        data.employee_id,
        db,
    )

    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )

    if not branch or branch.company_id != current_token["company_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot create a leave request for another company's employee",
        )

    leave_request = LeaveRequest(
        employee_id=data.employee_id,
        start_date=data.start_date,
        end_date=data.end_date,
        reason=data.reason,
        status="pending",
    )

    db.add(leave_request)
    db.commit()
    db.refresh(leave_request)

    return leave_request


@router.get("/")
def list_leave_requests(
    employee_id: int | None = None,
    status_filter: str | None = None,
    current_token: dict = Depends(require_roles("OWNER")),
    db: Session = Depends(get_db),
):
    query = db.query(LeaveRequest)

    if employee_id is not None:
        employee, department, branch = get_employee_company(
            employee_id,
            db,
        )

        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee not found",
            )

        if not branch or branch.company_id != current_token["company_id"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have access to this employee",
            )

        query = query.filter(
            LeaveRequest.employee_id == employee_id
        )

    else:
        company_employee_ids = (
            db.query(Employee.id)
            .join(
                Department,
                Department.id == Employee.department_id,
            )
            .join(
                Branch,
                Branch.id == Department.branch_id,
            )
            .filter(
                Branch.company_id == current_token["company_id"]
            )
            .all()
        )

        employee_ids = [item[0] for item in company_employee_ids]

        if not employee_ids:
            return []

        query = query.filter(
            LeaveRequest.employee_id.in_(employee_ids)
        )

    if status_filter is not None:
        allowed_statuses = {
            "pending",
            "approved",
            "rejected",
        }

        if status_filter not in allowed_statuses:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid leave request status",
            )

        query = query.filter(
            LeaveRequest.status == status_filter
        )

    return query.all()


@router.get("/{leave_request_id}")
def get_leave_request(
    leave_request_id: int,
    current_token: dict = Depends(require_roles("OWNER")),
    db: Session = Depends(get_db),
):
    leave_request = db.query(LeaveRequest).filter(
        LeaveRequest.id == leave_request_id
    ).first()

    if not leave_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Leave request not found",
        )

    employee, department, branch = get_employee_company(
        leave_request.employee_id,
        db,
    )

    if not branch or branch.company_id != current_token["company_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this leave request",
        )

    return leave_request


@router.patch("/{leave_request_id}")
def update_leave_request(
    leave_request_id: int,
    data: LeaveRequestUpdate,
    current_token: dict = Depends(require_roles("OWNER")),
    db: Session = Depends(get_db),
):
    leave_request = db.query(LeaveRequest).filter(
        LeaveRequest.id == leave_request_id
    ).first()

    if not leave_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Leave request not found",
        )

    employee, department, branch = get_employee_company(
        leave_request.employee_id,
        db,
    )

    if not branch or branch.company_id != current_token["company_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this leave request",
        )

    new_start_date = (
        data.start_date
        if data.start_date is not None
        else leave_request.start_date
    )

    new_end_date = (
        data.end_date
        if data.end_date is not None
        else leave_request.end_date
    )

    if new_end_date < new_start_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="End date cannot be before start date",
        )

    if data.start_date is not None:
        leave_request.start_date = data.start_date

    if data.end_date is not None:
        leave_request.end_date = data.end_date

    if data.reason is not None:
        leave_request.reason = data.reason

    db.commit()
    db.refresh(leave_request)

    return leave_request


@router.patch("/{leave_request_id}/status")
def update_leave_request_status(
    leave_request_id: int,
    data: LeaveRequestStatusUpdate,
    current_token: dict = Depends(require_roles("OWNER")),
    db: Session = Depends(get_db),
):
    leave_request = db.query(LeaveRequest).filter(
        LeaveRequest.id == leave_request_id
    ).first()

    if not leave_request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Leave request not found",
        )

    employee, department, branch = get_employee_company(
        leave_request.employee_id,
        db,
    )

    if not branch or branch.company_id != current_token["company_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this leave request",
        )

    if leave_request.status != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only pending leave requests can be approved or rejected",
        )

    leave_request.status = data.status
    leave_request.approved_by = current_token["user_id"]

    action = "APPROVE" if data.status == "approved" else "REJECT"
    details = "Leave request approved" if data.status == "approved" else "Leave request rejected"

    db.commit()
    log_action(db=db, user_id=current_token["user_id"], action=action, entity_type="LEAVE_REQUEST", entity_id=leave_request.id, details=details)
    db.refresh(leave_request)

    return leave_request
