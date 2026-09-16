from fastapi.responses import Response
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.authorization import require_roles
from app.db.database import get_db
from app.services.csv_export import export_to_csv
from app.services.employee_report import get_employee_report
from app.services.task_report import get_task_report
from app.services.branch_report import get_branch_report
from app.services.leave_report import get_leave_report
from app.models.report import Report
from app.models.branch import Branch
from app.schemas.report import (
    ReportCreate,
    ReportUpdate,
    ReportResponse,
    ReportStatusUpdate,
)

router = APIRouter(
    prefix="/reports",
    tags=["Reports"],
)


def check_branch_access(
    branch_id: int | None,
    company_id: int,
    db: Session,
):
    if branch_id is None:
        return None

    branch = db.query(Branch).filter(
        Branch.id == branch_id
    ).first()

    if not branch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Branch not found",
        )

    if branch.company_id != company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this branch",
        )

    return branch


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_report(
    data: ReportCreate,
    current_token: dict = Depends(require_roles("OWNER")),
    db: Session = Depends(get_db),
):
    check_branch_access(
        data.branch_id,
        current_token["company_id"],
        db,
    )

    report = Report(
        company_id=current_token["company_id"],
        branch_id=data.branch_id,
        created_by=current_token["user_id"],
        report_type=data.report_type,
        title=data.title,
        content=data.content,
        status="draft",
    )

    db.add(report)
    db.commit()
    db.refresh(report)

    return report


@router.get("/")
def list_reports(
    branch_id: int | None = None,
    status_filter: str | None = None,
    report_type: str | None = None,
    current_token: dict = Depends(require_roles("OWNER")),
    db: Session = Depends(get_db),
):
    query = db.query(Report).filter(
        Report.company_id == current_token["company_id"]
    )

    if branch_id is not None:
        check_branch_access(
            branch_id,
            current_token["company_id"],
            db,
        )
        query = query.filter(
            Report.branch_id == branch_id
        )

    if status_filter is not None:
        allowed_statuses = {
            "draft",
            "submitted",
            "approved",
            "rejected",
        }

        if status_filter not in allowed_statuses:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid report status",
            )

        query = query.filter(
            Report.status == status_filter
        )

    if report_type is not None:
        query = query.filter(
            Report.report_type == report_type
        )

    return query.all()


@router.get("/employees/export")
def export_employee_report(
    current_token: dict = Depends(require_roles("OWNER")),
    db: Session = Depends(get_db),
):
    company_id = current_token["company_id"]

    report = get_employee_report(
        db=db,
        company_id=company_id,
    )

    csv_data = export_to_csv(report["employees"])

    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=employees_report.csv"
        },
    )


@router.get("/employees")
def employee_report(
    current_token: dict = Depends(require_roles("OWNER")),
    db: Session = Depends(get_db),
):
    company_id = current_token["company_id"]

    return get_employee_report(
        db=db,
        company_id=company_id,
    )


@router.get("/tasks/export")
def export_task_report(
    current_token: dict = Depends(require_roles("OWNER")),
    db: Session = Depends(get_db),
):
    company_id = current_token["company_id"]

    report = get_task_report(
        db=db,
        company_id=company_id,
    )

    csv_data = export_to_csv(report["tasks"])

    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=tasks_report.csv"
        },
    )


@router.get("/tasks")
def task_report(
    current_token: dict = Depends(require_roles("OWNER")),
    db: Session = Depends(get_db),
):
    company_id = current_token["company_id"]

    return get_task_report(
        db=db,
        company_id=company_id,
    )


@router.get("/branches/export")
def export_branch_report(
    current_token: dict = Depends(require_roles("OWNER")),
    db: Session = Depends(get_db),
):
    company_id = current_token["company_id"]

    report = get_branch_report(
        db=db,
        company_id=company_id,
    )

    csv_data = export_to_csv(report["branches"])

    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=branches_report.csv"
        },
    )


@router.get("/branches")
def branch_report(
    current_token: dict = Depends(require_roles("OWNER")),
    db: Session = Depends(get_db),
):
    company_id = current_token["company_id"]

    return get_branch_report(
        db=db,
        company_id=company_id,
    )


@router.get("/leave-requests/export")
def export_leave_report(
    current_token: dict = Depends(require_roles("OWNER")),
    db: Session = Depends(get_db),
):
    company_id = current_token["company_id"]

    report = get_leave_report(
        db=db,
        company_id=company_id,
    )

    csv_data = export_to_csv(report["leave_requests"])

    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=leave_requests_report.csv"
        },
    )


@router.get("/leave-requests")
def leave_report(
    current_token: dict = Depends(require_roles("OWNER")),
    db: Session = Depends(get_db),
):
    company_id = current_token["company_id"]

    return get_leave_report(
        db=db,
        company_id=company_id,
    )


@router.get("/{report_uuid}", response_model=ReportResponse)
def get_report(
    report_uuid: str,
        current_token: dict = Depends(require_roles("OWNER")),
    db: Session = Depends(get_db),
):
    report = db.query(Report).filter(
        Report.uuid == report_uuid
    ).first()

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found",
        )

    if report.company_id != current_token["company_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this report",
        )

    return report


@router.patch("/{report_uuid}", response_model=ReportResponse)
def update_report(
    report_uuid: str,
    data: ReportUpdate,
    current_token: dict = Depends(require_roles("OWNER")),
    db: Session = Depends(get_db),
):
    report = db.query(Report).filter(
        Report.uuid == report_uuid
    ).first()

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found",
        )

    if report.company_id != current_token["company_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this report",
        )

    if data.branch_id is not None:
        check_branch_access(
            data.branch_id,
            current_token["company_id"],
            db,
        )
        report.branch_id = data.branch_id

    if data.report_type is not None:
        report.report_type = data.report_type

    if data.title is not None:
        report.title = data.title

    if data.content is not None:
        report.content = data.content

    db.commit()
    db.refresh(report)

    return report


@router.patch("/{report_uuid}/status", response_model=ReportResponse)
def update_report_status(
    report_uuid: str,
    data: ReportStatusUpdate,
    current_token: dict = Depends(require_roles("OWNER")),
    db: Session = Depends(get_db),
):
    report = db.query(Report).filter(
        Report.uuid == report_uuid
    ).first()

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found",
        )

    if report.company_id != current_token["company_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this report",
        )

    report.status = data.status

    db.commit()
    db.refresh(report)

    return report
