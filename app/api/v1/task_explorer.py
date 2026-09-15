from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.authorization import require_roles
from app.db.database import get_db
from app.services.task_explorer import search_tasks


router = APIRouter(
    prefix="/task-explorer",
    tags=["Task Explorer"],
)


@router.get("/tasks")
def explore_tasks(
    search: str | None = Query(default=None),
    status: str | None = Query(default=None),
    priority: str | None = Query(default=None),
    employee_id: int | None = Query(default=None),
    current_token: dict = Depends(require_roles("OWNER")),
    db: Session = Depends(get_db),
):
    company_id = current_token["company_id"]

    tasks = search_tasks(
        db=db,
        company_id=company_id,
        search=search,
        status=status,
        priority=priority,
        employee_id=employee_id,
    )

    return {
        "company_id": company_id,
        "count": len(tasks),
        "tasks": [
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "status": task.status,
                "priority": task.priority,
                "assigned_to": task.assigned_to,
            }
            for task in tasks
        ],
    }
