from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.authorization import require_roles
from app.db.database import get_db
from app.models.task import Task
from app.models.task_history import TaskHistory
from app.models.employee import Employee
from app.models.department import Department
from app.models.branch import Branch
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskStatusUpdate

router = APIRouter(prefix="/tasks", tags=["Tasks"])


def get_employee_company(
    employee_id: int,
    db: Session,
):
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


@router.get("/")
def list_tasks(
    assigned_to: int | None = None,
    status_filter: str | None = None,
    current_token: dict = Depends(require_roles("OWNER")),
    db: Session = Depends(get_db),
):
    query = db.query(Task)

    if assigned_to is not None:
        employee, department, branch = get_employee_company(
            assigned_to,
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

        query = query.filter(Task.assigned_to == assigned_to)

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

        query = query.filter(Task.assigned_to.in_(employee_ids))

    if status_filter is not None:
        allowed_statuses = {
            "pending",
            "in_progress",
            "completed",
            "cancelled",
        }

        if status_filter not in allowed_statuses:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid task status",
            )

        query = query.filter(Task.status == status_filter)

    return query.all()


@router.get("/{task_uuid}", response_model=TaskResponse)
def get_task(
    task_uuid: str,
    current_token: dict = Depends(require_roles("OWNER")),
    db: Session = Depends(get_db),
):
    task = db.query(Task).filter(
        Task.uuid == task_uuid
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    employee, department, branch = get_employee_company(
        task.assigned_to,
        db,
    )

    if not branch or branch.company_id != current_token["company_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this task",
        )

    return task


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_task(
    data: TaskCreate,
    current_token: dict = Depends(require_roles("OWNER")),
    db: Session = Depends(get_db),
):
    employee, department, branch = get_employee_company(
        data.assigned_to,
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
            detail="You cannot assign a task to another company's employee",
        )

    task = Task(
        title=data.title,
        description=data.description,
        created_by=current_token["user_id"],
        assigned_to=data.assigned_to,
        priority=data.priority,
        status="pending",
        due_date=data.due_date,
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    history = TaskHistory(
        task_id=task.id,
        changed_by=current_token["user_id"],
        old_status=None,
        new_status="pending",
        note="Task created",
    )

    db.add(history)
    db.commit()

    return task


@router.patch("/{task_uuid}", response_model=TaskResponse)
def update_task(
    task_uuid: str,
    data: TaskUpdate,
    current_token: dict = Depends(require_roles("OWNER")),
    db: Session = Depends(get_db),
):
    task = db.query(Task).filter(
        Task.uuid == task_uuid
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    employee, department, branch = get_employee_company(
        task.assigned_to,
        db,
    )

    if not branch or branch.company_id != current_token["company_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this task",
        )

    if data.assigned_to is not None:
        new_employee, new_department, new_branch = get_employee_company(
            data.assigned_to,
            db,
        )

        if not new_employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="New employee not found",
            )

        if (
            not new_branch
            or new_branch.company_id != current_token["company_id"]
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You cannot assign a task to another company's employee",
            )

        task.assigned_to = data.assigned_to

    if data.title is not None:
        task.title = data.title

    if data.description is not None:
        task.description = data.description

    if data.priority is not None:
        task.priority = data.priority

    if data.due_date is not None:
        task.due_date = data.due_date

    if data.status is not None and data.status != task.status:
        old_status = task.status
        task.status = data.status

        history = TaskHistory(
            task_id=task.id,
            changed_by=current_token["user_id"],
            old_status=old_status,
            new_status=data.status,
            note="Task status updated",
        )

        db.add(history)

    db.commit()
    db.refresh(task)

    return task


@router.patch("/{task_uuid}/status", response_model=TaskResponse)
def update_task_status(
    task_uuid: str,
    data: TaskStatusUpdate,
    current_token: dict = Depends(require_roles("OWNER")),
    db: Session = Depends(get_db),
):
    task = db.query(Task).filter(
        Task.uuid == task_uuid
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    employee, department, branch = get_employee_company(
        task.assigned_to,
        db,
    )

    if not branch or branch.company_id != current_token["company_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this task",
        )

    if data.status == task.status:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task is already in this status",
        )

    old_status = task.status
    task.status = data.status

    history = TaskHistory(
        task_id=task.id,
        changed_by=current_token["user_id"],
        old_status=old_status,
        new_status=data.status,
        note=data.note,
    )

    db.add(history)
    db.commit()
    db.refresh(task)

    return task
