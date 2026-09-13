from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.authorization import require_roles
from app.db.database import get_db
from app.models.audit_log import AuditLog
from app.models.user import User

router = APIRouter(
    prefix="/audit-logs",
    tags=["Audit Logs"],
)


@router.get("/")
def list_audit_logs(
    current_token: dict = Depends(require_roles("OWNER")),
    db: Session = Depends(get_db),
):
    company_id = current_token["company_id"]

    logs = (
        db.query(AuditLog)
        .join(User, AuditLog.user_id == User.id)
        .filter(User.company_id == company_id)
        .order_by(AuditLog.created_at.desc())
        .all()
    )

    return logs
