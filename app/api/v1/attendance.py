from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.authorization import require_roles
from app.db.database import get_db
from app.models.attendance import Attendance
from app.models.employee import Employee
from app.models.department import Department
from app.models.branch import Branch
from app.schemas.attendance import AttendanceCreate, AttendanceUpdate, AttendanceResponse

router = APIRouter(prefix="/attendance", tags=["Attendance"])


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
def create_attendance(
    data: AttendanceCreate,
    current_token: dict = Depends(require_roles("OWNER")),
    db: Session = Depends(get_db),
):
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
            detail="You cannot create attendance for another company's employee",
        )

    attendance = Attendance(
        employee_id=data.employee_id,
        check_in=data.check_in,
        status="present",
        note=data.note,
    )

    db.add(attendance)
    db.commit()
    db.refresh(attendance)

    return attendance


@router.get("/", response_model=list[AttendanceResponse])
def list_attendance(
    employee_id: int | None = None,
    current_token: dict = Depends(require_roles("OWNER")),
    db: Session = Depends(get_db),
):
    query = db.query(Attendance)

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
            Attendance.employee_id == employee_id
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
            Attendance.employee_id.in_(employee_ids)
        )

    return query.all()


@router.get("/{attendance_uuid}", response_model=AttendanceResponse)
def get_attendance(
    attendance_uuid: str,
    current_token: dict = Depends(require_roles("OWNER")),
    db: Session = Depends(get_db),
):
    attendance = db.query(Attendance).filter(
        Attendance.uuid == attendance_uuid
    ).first()

    if not attendance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance record not found",
        )

    employee, department, branch = get_employee_company(
        attendance.employee_id,
        db,
    )

    if not branch or branch.company_id != current_token["company_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this attendance record",
        )

    return attendance


@router.patch("/{attendance_uuid}", response_model=AttendanceResponse)
def update_attendance(
    attendance_uuid: str,
    data: AttendanceUpdate,
    current_token: dict = Depends(require_roles("OWNER")),
    db: Session = Depends(get_db),
):
    attendance = db.query(Attendance).filter(
        Attendance.uuid == attendance_uuid
    ).first()

    if not attendance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance record not found",
        )

    employee, department, branch = get_employee_company(
        attendance.employee_id,
        db,
    )

    if not branch or branch.company_id != current_token["company_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this attendance record",
        )

    if data.check_in is not None:
        attendance.check_in = data.check_in

    if data.check_out is not None:
        attendance.check_out = data.check_out

    if data.status is not None:
        attendance.status = data.status

    if data.note is not None:
        attendance.note = data.note

    db.commit()
    db.refresh(attendance)

    return attendance
