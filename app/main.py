from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router
from app.api.v1.companies import router as companies_router
from app.api.v1.branches import router as branches_router
from app.api.v1.departments import router as departments_router
from app.api.v1.employees import router as employees_router
from app.api.v1.tasks import router as tasks_router
from app.api.v1.attendance import router as attendance_router
from app.api.v1.leave_requests import router as leave_requests_router
from app.api.v1.reports import router as reports_router
from app.api.v1.notifications import router as notifications_router
from app.api.v1.dashboard import router as dashboard_router
from app.api.v1.audit_logs import router as audit_logs_router

app = FastAPI(
    title="Central Company Management System",
    description="Centralized management system for multi-branch companies",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:5174", "http://127.0.0.1:5174", "http://localhost:5175", "http://127.0.0.1:5175", "http://localhost:5176", "http://127.0.0.1:5176"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")
app.include_router(companies_router, prefix="/api/v1")
app.include_router(branches_router, prefix="/api/v1")
app.include_router(departments_router, prefix="/api/v1")
app.include_router(employees_router, prefix="/api/v1")
app.include_router(tasks_router, prefix="/api/v1")
app.include_router(attendance_router, prefix="/api/v1")
app.include_router(leave_requests_router, prefix="/api/v1")
app.include_router(reports_router, prefix="/api/v1")
app.include_router(notifications_router, prefix="/api/v1")
app.include_router(dashboard_router, prefix="/api/v1")
app.include_router(audit_logs_router, prefix="/api/v1")


@app.get("/")
def root():
    return {"message": "Central Company Management System API is running"}
