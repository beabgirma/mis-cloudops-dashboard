services=[]
next_service_id=1

def reset_services():
    global next_service_id
    services.clear()
    next_service_id=1

def create_service_record(service):
    global next_service_id
    new_service={
        "id": next_service_id,
        "name": service.name,
        "url": service.url,
        "owner": service.owner,
        "status":"unknown"
    }
    services.append(new_service)
    next_service_id+=1
    return  new_service 

def list_service_records():
    return services

def update_service_status_record(service_id: int, status: str):
    for service in services:
        if service["id"]== service_id:
            service["status"]=status
            return service
    return None


