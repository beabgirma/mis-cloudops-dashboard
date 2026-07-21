from fastapi import FastAPI
from app.routers import services_router
from app.database import init_db
import asyncio
from contextlib import asynccontextmanager
from service.service import periodic_health_checks

@asynccontextmanager
async def lifespan(app: FastAPI):
    bg_task = asyncio.create_task(periodic_health_checks())
    yield 
    bg_task.cancel()

app = FastAPI(title="MIS CloudOps Dashboard", lifespan=lifespan)

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




