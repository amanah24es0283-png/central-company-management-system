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
