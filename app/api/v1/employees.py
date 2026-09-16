from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.authorization import require_roles
from app.db.database import get_db
from app.models.employee import Employee
from app.models.user import User
from app.models.department import Department
from app.models.branch import Branch
from app.schemas.employee import EmployeeCreate, EmployeeUpdate, EmployeeResponse

router = APIRouter(prefix="/employees", tags=["Employees"])


@router.get("/")
def list_employees(
    department_id: int | None = None,
    current_token: dict = Depends(require_roles("OWNER")),
    db: Session = Depends(get_db),
):
    query = (
        db.query(Employee)
        .join(Department, Employee.department_id == Department.id)
        .join(Branch, Department.branch_id == Branch.id)
        .filter(Branch.company_id == current_token["company_id"])
    )

    if department_id is not None:
        query = query.filter(Employee.department_id == department_id)

    return query.all()


@router.get("/{employee_uuid}", response_model=EmployeeResponse)
def get_employee(
    employee_uuid: str,
    current_token: dict = Depends(require_roles("OWNER")),
    db: Session = Depends(get_db),
):
    employee = db.query(Employee).filter(
        Employee.uuid == employee_uuid
    ).first()

    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )

    department = db.query(Department).filter(
        Department.id == employee.department_id
    ).first()

    branch = db.query(Branch).filter(
        Branch.id == department.branch_id
    ).first() if department else None

    if not branch or branch.company_id != current_token["company_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this employee",
        )

    return employee


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_employee(
    data: EmployeeCreate,
    current_token: dict = Depends(require_roles("OWNER")),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(
        User.id == data.user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    if user.company_id != current_token["company_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot assign a user from another company",
        )

    department = db.query(Department).filter(
        Department.id == data.department_id
    ).first()

    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found",
        )

    branch = db.query(Branch).filter(
        Branch.id == department.branch_id
    ).first()

    if not branch or branch.company_id != current_token["company_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot create an employee in another company's department",
        )

    existing_employee = db.query(Employee).filter(
        Employee.user_id == data.user_id
    ).first()

    if existing_employee:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User is already assigned as an employee",
        )

    existing_code = db.query(Employee).filter(
        Employee.employee_code == data.employee_code
    ).first()

    if existing_code:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Employee code already exists",
        )

    employee = Employee(
        user_id=data.user_id,
        department_id=data.department_id,
        employee_code=data.employee_code,
        job_title=data.job_title,
        phone=data.phone,
        hire_date=data.hire_date,
        status="active",
    )

    db.add(employee)
    db.commit()
    db.refresh(employee)

    return employee


@router.patch("/{employee_uuid}", response_model=EmployeeResponse)
def update_employee(
    employee_uuid: str,
    data: EmployeeUpdate,
    current_token: dict = Depends(require_roles("OWNER")),
    db: Session = Depends(get_db),
):
    employee = db.query(Employee).filter(
        Employee.uuid == employee_uuid
    ).first()

    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found",
        )

    department = db.query(Department).filter(
        Department.id == employee.department_id
    ).first()

    branch = db.query(Branch).filter(
        Branch.id == department.branch_id
    ).first() if department else None

    if not branch or branch.company_id != current_token["company_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this employee",
        )

    if data.department_id is not None:
        new_department = db.query(Department).filter(
            Department.id == data.department_id
        ).first()

        if not new_department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="New department not found",
            )

        new_branch = db.query(Branch).filter(
            Branch.id == new_department.branch_id
        ).first()

        if not new_branch or new_branch.company_id != current_token["company_id"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You cannot move an employee to another company's department",
            )

        employee.department_id = data.department_id

    if data.employee_code is not None:
        existing_code = db.query(Employee).filter(
            Employee.employee_code == data.employee_code,
            Employee.id != employee_id,
        ).first()

        if existing_code:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Employee code already exists",
            )

        employee.employee_code = data.employee_code

    if data.job_title is not None:
        employee.job_title = data.job_title

    if data.phone is not None:
        employee.phone = data.phone

    if data.hire_date is not None:
        employee.hire_date = data.hire_date

    if data.status is not None:
        employee.status = data.status

    db.commit()
    db.refresh(employee)

    return employee
