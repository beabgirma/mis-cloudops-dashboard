from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.routers import services_router
from app.repositories.service_repo import list_service_records
from app.database import init_db

# 1. Database and App Lifespan Management
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

# 2. Application Initialization
app = FastAPI(title="MIS CloudOps Dashboard", lifespan=lifespan)

# 3. Template Configuration & Router Registration
templates = Jinja2Templates(directory="app/templates")
app.include_router(services_router.router)

# 4. Root Dashboard View Route
@app.get("/", response_class=HTMLResponse)
async def read_dashboard(request: Request):
    db_services = list_service_records()
    
    # Calculate global metrics
    total_services = len(db_services)
    
    # Safely extract status whether the service is an object or a dictionary
    def get_status(s):
        return getattr(s, 'status', None) or (s.get('status') if isinstance(s, dict) else None)
        
    active_services = sum(1 for s in db_services if get_status(s) == 'operational')
    
    # Determine global system status for the template's metrics block
    # If there are services and all of them are operational, system is Operational. Otherwise, Degraded.
    if total_services > 0 and active_services == total_services:
        system_status = "Operational"
    else:
        system_status = "Degraded"

    # Wrap inside the 'metrics' object the template expects
    metrics = {
        "status": system_status
    }

    return templates.TemplateResponse(
        request, 
        "dashboard.html", 
        {
            "total_services": total_services,
            "active_services": active_services,
            "db_services": db_services,
            "metrics": metrics
        }
    )