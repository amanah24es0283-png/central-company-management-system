from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.authorization import require_roles
from app.db.database import get_db
from app.models.department import Department
from app.models.branch import Branch
from app.schemas.department import DepartmentCreate, DepartmentUpdate, DepartmentResponse

router = APIRouter(prefix="/departments", tags=["Departments"])


@router.get("/")
def list_departments(
    branch_id: int | None = None,
    current_token: dict = Depends(require_roles("OWNER")),
    db: Session = Depends(get_db),
):
    query = (
        db.query(Department)
        .join(Branch, Department.branch_id == Branch.id)
        .filter(Branch.company_id == current_token["company_id"])
    )

    if branch_id is not None:
        query = query.filter(Department.branch_id == branch_id)

    return query.all()


@router.get("/{department_uuid}", response_model=DepartmentResponse)
def get_department(
    department_uuid: str,
    current_token: dict = Depends(require_roles("OWNER")),
    db: Session = Depends(get_db),
):
    department = db.query(Department).filter(
        Department.uuid == department_uuid
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
            detail="You do not have access to this department",
        )

    return department


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_department(
    data: DepartmentCreate,
    current_token: dict = Depends(require_roles("OWNER")),
    db: Session = Depends(get_db),
):
    branch = db.query(Branch).filter(
        Branch.id == data.branch_id
    ).first()

    if not branch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Branch not found",
        )

    if branch.company_id != current_token["company_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot create a department in another company's branch",
        )

    department = Department(
        branch_id=data.branch_id,
        name=data.name,
        description=data.description,
        manager_id=data.manager_id,
    )

    db.add(department)
    db.commit()
    db.refresh(department)

    return department


@router.patch("/{department_uuid}", response_model=DepartmentResponse)
def update_department(
    department_uuid: str,
    data: DepartmentUpdate,
    current_token: dict = Depends(require_roles("OWNER")),
    db: Session = Depends(get_db),
):
    department = db.query(Department).filter(
        Department.uuid == department_uuid
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
            detail="You do not have access to this department",
        )

    if data.name is not None:
        department.name = data.name

    if data.description is not None:
        department.description = data.description

    if data.manager_id is not None:
        department.manager_id = data.manager_id

    db.commit()
    db.refresh(department)

    return department
