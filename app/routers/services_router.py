from fastapi import APIRouter, HTTPException
from app.schemas.service_schema import ServiceCreate, ServiceStatusUpdate
from app.services import service_service

router= APIRouter()

@router.post("/services",status_code=201)
def create_service(service: ServiceCreate):
    return service_service.create_service(service)

@router.get("/services")
def list_services():
    return service_service.list_services()

@router.patch("/services/{service_id}/status")
def update_service_status(service_id: int, update: ServiceStatusUpdate):
    updated_service=service_service.update_service_status(service_id, update)

    if updated_service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    return updated_service

@router.get("/services/{service_id}")
def get_service_by_id(service_id:int):
    service_by_id=service_service.get_service_by_id(service_id)

    if service_by_id is None:
        raise HTTPException(status_code=404, detail="Service not found")
    return service_by_id

"""1. Receive service_id as an int
2. Call service_service.delete_service_by_id(service_id)
3. If the result is None, raise 404 with "Service not found"
4. Otherwise return the deleted service"""

@router.delete("/services/{service_id}")
def delete_service_by_id(service_id:int):
    service_by_id=service_service.delete_service_by_id(service_id)
    if service_by_id is None:
        raise HTTPException(status_code=404, detail="Service not found")
    return service_by_id
