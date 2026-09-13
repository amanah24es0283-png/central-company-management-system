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
