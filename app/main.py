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
