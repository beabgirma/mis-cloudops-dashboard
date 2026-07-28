import asyncio
import subprocess
import os
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from types import SimpleNamespace

from app.database import init_db
from app.repositories.service_repo import list_service_records, create_service_record
from app.health_checker import monitor_services_loop
from app.redis_client import send_redis_command
from app.routers.services_router import router as services_router

redis_process = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    app_dir = os.path.dirname(os.path.abspath(__file__))               # app/
    project_root = os.path.dirname(app_dir)                            # MIS-cloud-dashboard/
    parent_dir = os.path.dirname(project_root)                         # Sibling container folder

    # Strategy A: Look for it as a sibling directory
    redis_script_path = os.path.join(parent_dir, "mini-redis", "server.py")

    # Strategy B: Fallback if mini-redis is inside the dashboard folder (this will trip now!)
    if not os.path.exists(redis_script_path):
        redis_script_path = os.path.join(project_root, "mini-redis", "server.py")
    
    if os.path.exists(redis_script_path):
        redis_process = subprocess.Popen(
            [sys.executable, redis_script_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        # Give the TCP port listener a moment to initialize and bind
        await asyncio.sleep(1.0)

    # Setup standard SQLite table structure
    init_db()

    # Spin up the background network URL ping daemon loop
    asyncio.create_task(monitor_services_loop())

    yield

    # Clean shutdown of the Redis sub-process engine
    if redis_process:
        redis_process.terminate()
        redis_process.wait()

app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory="app/templates")

# Mount dynamic routers
app.include_router(services_router)

@app.get("/", response_class=HTMLResponse)
async def read_dashboard(request: Request):
    # Fetch active assets out of SQLite persistence engine
    services_list = list_service_records()
    
    enriched_services = []
    total_count = len(services_list)
    healthy_count = 0
    unhealthy_count = 0

    for s in services_list:
        # Pull ephemeral real-time health updates out of the Redis structures using the aligned pattern
        status = send_redis_command(f"GET service:{s['id']}:status")
        if not status:
            status = "REDIS_DOWN"
        
        if status == "Healthy":
            healthy_count += 1
        elif status == "Unhealthy":
            unhealthy_count += 1

        enriched_services.append({
            "id": s["id"],
            "name": s["name"],
            "url": s["url"],
            "owner": s["owner"],
            "status": status
        })

    metrics = {
        "total": total_count,
        "healthy": healthy_count,
        "unhealthy": unhealthy_count
    }

    # Pass request as the first positional argument to clear deprecation warnings cleanly
    return templates.TemplateResponse(
        request,
        "dashboard.html",
        {
            "services": enriched_services,
            "metrics": metrics
        }
    )

@app.post("/services/add")
async def add_new_service(
    name: str = Form(...),
    url: str = Form(...),
    owner: str = Form(...)
):
    """Inserts a user-submitted service asset using SimpleNamespace to match dot-notation requirements."""
    service_data = SimpleNamespace(
        name=name,
        url=url,
        owner=owner
    )
    
    create_service_record(service_data)

    # Redirect back to home screen to refresh dashboard stats instantly
    return RedirectResponse(url="/", status_code=303)