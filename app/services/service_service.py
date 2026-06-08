from app.repositories import service_repo


def create_service(service):
    return service_repo.create_service_record(service)


def list_services():
    return {
        "services": service_repo.list_service_records()
    }


def update_service_status(service_id:int, update):
    return service_repo.update_service_status_record(
        service_id,
        update.status
    )

def get_service_by_id(service_id:int):
    return service_repo.get_service_by_id(
        service_id
    )

def delete_service_by_id(service_id:int ):
    return service_repo.delete_service_by_id(
        service_id
    )
