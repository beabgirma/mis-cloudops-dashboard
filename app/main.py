from fastapi import FastAPI
from app.routers import services_router
from app.database import init_db

app = FastAPI(title="MIS CloudOps Dashboard")

app.include_router(services_router.router)


@app.get("/")
def root():
    return {
        "message": "Welcome to MIS CloudOps Dashboard",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "mis-cloudops-dashboard"
    }

init_db()
