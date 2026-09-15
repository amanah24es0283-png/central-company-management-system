from sqlalchemy.orm import Session

from app.services.analytics import get_company_analytics
from app.services.analytics import get_employee_distribution_by_branch
from app.services.analytics import get_employee_performance
from app.services.analytics import get_leave_analytics


def get_advanced_dashboard(
    db: Session,
    company_id: int,
):
    company = get_company_analytics(
        db=db,
        company_id=company_id,
    )

    employee_performance = get_employee_performance(
        db=db,
        company_id=company_id,
    )

    branch_distribution = get_employee_distribution_by_branch(
        db=db,
        company_id=company_id,
    )

    leave_analytics = get_leave_analytics(
        db=db,
        company_id=company_id,
    )

    return {
        "company_id": company_id,
        "summary": company["summary"],
        "employee_performance": employee_performance["employees"],
        "branch_distribution": branch_distribution["branches"],
        "leave_analytics": leave_analytics["leave_requests"],
    }
