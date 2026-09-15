from fastapi import FastAPI

app = FastAPI(
    title="Central Company Management System",
    description="Centralized management system for multi-branch companies",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "message": "Central Company Management System API is running"
    }

from app.api.v1.auth import router as auth_router

app.include_router(
    auth_router,
    prefix="/api/v1"
)

from app.api.v1.companies import router as companies_router

app.include_router(
    companies_router,
    prefix="/api/v1"
)

from app.api.v1.branches import router as branches_router

app.include_router(
    branches_router,
    prefix="/api/v1"
)

from app.api.v1.departments import router as departments_router

app.include_router(
    departments_router,
    prefix="/api/v1"
)

from app.api.v1.employees import router as employees_router

app.include_router(
    employees_router,
    prefix="/api/v1"
)

from app.api.v1.tasks import router as tasks_router

app.include_router(
    tasks_router,
    prefix="/api/v1"
)

from app.api.v1.attendance import router as attendance_router

app.include_router(
    attendance_router,
    prefix="/api/v1"
)

from app.api.v1.leave_requests import router as leave_requests_router

app.include_router(
    leave_requests_router,
    prefix="/api/v1"
)

from app.api.v1.reports import router as reports_router

app.include_router(
    reports_router,
    prefix="/api/v1"
)

from app.api.v1.notifications import router as notifications_router

app.include_router(
    notifications_router,
    prefix="/api/v1"
)


from app.api.v1.dashboard import router as dashboard_router

app.include_router(
    dashboard_router,
    prefix="/api/v1"
)


from app.api.v1.audit_logs import router as audit_logs_router
from app.api.v1.analytics import router as analytics_router
from app.api.v1.data_explorer import router as data_explorer_router
from app.api.v1.task_explorer import router as task_explorer_router
from app.api.v1.branch_explorer import router as branch_explorer_router

app.include_router(
    audit_logs_router,
    prefix="/api/v1"
)

app.include_router(
    analytics_router,
    prefix="/api/v1"
)

app.include_router(
    data_explorer_router,
    prefix="/api/v1"
)
app.include_router(
    task_explorer_router,
    prefix="/api/v1"
)
app.include_router(
    branch_explorer_router,
    prefix="/api/v1"
)
