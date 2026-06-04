from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="MIS CloudOps Dashboard")

class ServiceCreate(BaseModel):
    name:str
    url:str
    owner:str = "MIS Team"

services = []
next_service_id =1


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

@app.post("/services", status_code=201)
def create_service(service: ServiceCreate):
    global next_service_id

    new_service={
        "id": next_service_id,
        "name":service.name,
        "url":service.url,
        "owner":service.owner,
        "status":"unknown"
    }
    services.append(new_service)
    next_service_id+=1
    return new_service

@app.get("/services")
def list_services():
    return {
        "services": services
    }