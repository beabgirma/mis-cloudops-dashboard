from app.repositories import service_repo


def create_service(service):
    return service_repo.create_service_record(service)


def list_services():
    return {
        "services": service_repo.list_service_records()
    }


def update_service_status(service_id, update):
    return service_repo.update_service_status_record(
        service_id,
        update.status
    )